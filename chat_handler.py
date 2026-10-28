"""Prank chat: ada pesan masuk -> delay acak -> mengetik... -> berhenti -> offline. Tidak pernah membalas/membaca."""
import asyncio
import logging
import random
import time

from telethon import TelegramClient, events

import config
from presence import set_offline, set_online

log = logging.getLogger(__name__)

_busy: set[int] = set()
_last_prank: dict[int, float] = {}


def _rand(a: float, b: float) -> float:
    lo, hi = sorted((a, b))
    return random.uniform(lo, hi)


async def _creepy_typing(client: TelegramClient, chat_id: int) -> None:
    await asyncio.sleep(_rand(config.CHAT_DELAY_MIN, config.CHAT_DELAY_MAX))

    await set_online(client)
    bursts = random.randint(*sorted((config.BURSTS_MIN, config.BURSTS_MAX)))
    for i in range(bursts):
        async with client.action(chat_id, "typing"):
            await asyncio.sleep(_rand(config.TYPING_MIN, config.TYPING_MAX))
        if i < bursts - 1:
            # berhenti sejenak, lalu mengetik lagi
            await asyncio.sleep(_rand(1.5, 6))

    await asyncio.sleep(_rand(0.5, 2))
    await set_offline(client)


def register(client: TelegramClient) -> None:
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def on_message(event):
        sender = await event.get_sender()
        if not sender or getattr(sender, "bot", False):
            return

        uid = sender.id
        if config.ALLOWED_IDS and uid not in config.ALLOWED_IDS:
            return
        if uid in _busy:
            return
        if time.monotonic() - _last_prank.get(uid, 0) < config.CHAT_COOLDOWN:
            return

        _busy.add(uid)
        try:
            log.info("Chat dari %s, mulai prank mengetik", uid)
            await _creepy_typing(client, event.chat_id)
        except Exception as e:
            log.error("Prank chat error: %s", e)
        finally:
            _busy.discard(uid)
            _last_prank[uid] = time.monotonic()
