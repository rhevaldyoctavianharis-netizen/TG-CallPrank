"""Logika telepon masuk: angkat -> main.mp3 -> audio seram acak berulang -> tutup setelah batas waktu."""
import asyncio
import logging
import random
import time
from dataclasses import dataclass, field

from pytgcalls import PyTgCalls, filters
from pytgcalls.types import ChatUpdate, MediaStream, StreamEnded

import config
from audio_manager import RandomAudioBag, load_disturbing_files

log = logging.getLogger(__name__)


@dataclass
class CallSession:
    user_id: int
    bag: RandomAudioBag
    started: float = field(default_factory=time.monotonic)
    watchdog: asyncio.Task | None = None
    active: bool = True

    @property
    def elapsed(self) -> float:
        return time.monotonic() - self.started


sessions: dict[int, CallSession] = {}


def _audio_stream(path) -> MediaStream:
    # audio saja, tanpa video
    return MediaStream(str(path), video_flags=MediaStream.Flags.IGNORE)


async def _end_call(call_py: PyTgCalls, user_id: int, reason: str) -> None:
    sess = sessions.pop(user_id, None)
    if not sess:
        return
    sess.active = False
    if sess.watchdog and sess.watchdog is not asyncio.current_task():
        sess.watchdog.cancel()
    try:
        await call_py.leave_call(user_id)
    except Exception as e:
        log.debug("leave_call: %s", e)
    log.info("Telepon dengan %s selesai (%s, %.0f detik)", user_id, reason, sess.elapsed)


async def _watchdog(call_py: PyTgCalls, sess: CallSession) -> None:
    """Tutup telepon paksa saat batas waktu tercapai (walau audio belum selesai)."""
    await asyncio.sleep(config.MAX_CALL_SECONDS)
    await _end_call(call_py, sess.user_id, "batas waktu")


def register(call_py: PyTgCalls) -> None:
    disturbing = load_disturbing_files()
    log.info("%d audio seram dimuat", len(disturbing))

    # ---- telepon masuk ----
    @call_py.on_update(filters.chat_update(ChatUpdate.Status.INCOMING_CALL))
    async def on_incoming(_, update: ChatUpdate):
        user_id = update.chat_id
        if config.ALLOWED_IDS and user_id not in config.ALLOWED_IDS:
            return
        if user_id in sessions:
            return

        sess = CallSession(user_id=user_id, bag=RandomAudioBag(disturbing))
        sessions[user_id] = sess
        log.info("Telepon masuk dari %s", user_id)

        try:
            # play() pada telepon masuk = mengangkat telepon
            await call_py.play(user_id, _audio_stream(config.MAIN_AUDIO))
        except Exception as e:
            log.error("Gagal mengangkat telepon: %s", e)
            sessions.pop(user_id, None)
            return

        sess.watchdog = asyncio.create_task(_watchdog(call_py, sess))

    # ---- satu audio selesai -> putar audio acak berikutnya ----
    @call_py.on_update(filters.stream_end)
    async def on_stream_end(_, update: StreamEnded):
        sess = sessions.get(update.chat_id)
        if not sess or not sess.active:
            return

        if sess.elapsed >= config.MAX_CALL_SECONDS:
            await _end_call(call_py, sess.user_id, "batas waktu")
            return

        # jeda hening acak biar makin creepy
        lo, hi = sorted((config.GAP_MIN, config.GAP_MAX))
        await asyncio.sleep(random.uniform(lo, hi))
        if not sess.active:
            return

        nxt = sess.bag.next()
        if nxt is None:
            log.warning("Tidak ada audio seram, menutup telepon")
            await _end_call(call_py, sess.user_id, "tidak ada audio")
            return

        log.info("Memutar: %s", nxt.name)
        try:
            await call_py.play(sess.user_id, _audio_stream(nxt))
        except Exception as e:
            log.error("Gagal memutar %s: %s", nxt.name, e)
            await _end_call(call_py, sess.user_id, "error")

    # ---- penelepon menutup ----
    closed = (
        ChatUpdate.Status.DISCARDED_CALL
        | ChatUpdate.Status.LEFT_CALL
        | ChatUpdate.Status.CLOSED_VOICE_CHAT
    )

    @call_py.on_update(filters.chat_update(closed))
    async def on_closed(_, update: ChatUpdate):
        await _end_call(call_py, update.chat_id, "ditutup penelepon")
