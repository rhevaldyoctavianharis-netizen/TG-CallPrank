"""Pemilihan audio: main.mp3 + audio seram acak (shuffle bag, tanpa pengulangan beruntun)."""
import logging
import random
from pathlib import Path

import config

log = logging.getLogger(__name__)


def load_disturbing_files() -> list[Path]:
    """Ambil daftar audio seram dari config, atau scan folder assets."""
    if config.DISTURBING_AUDIOS:
        files = [config.ASSETS_DIR / name for name in config.DISTURBING_AUDIOS]
    else:
        files = [
            p
            for p in sorted(config.ASSETS_DIR.iterdir())
            if p.suffix.lower() in config.AUDIO_EXTS and p.name != config.MAIN_AUDIO.name
        ]

    valid = [p for p in files if p.exists()]
    missing = [p.name for p in files if not p.exists()]
    if missing:
        log.warning("File audio tidak ditemukan, dilewati: %s", ", ".join(missing))
    return valid


class RandomAudioBag:
    """Acak seperti mengocok kartu: semua audio keluar dulu sebelum diulang."""

    def __init__(self, files: list[Path]):
        self._files = list(files)
        self._bag: list[Path] = []
        self._last: Path | None = None

    def next(self) -> Path | None:
        if not self._files:
            return None
        if not self._bag:
            self._bag = self._files[:]
            random.shuffle(self._bag)
            # hindari audio yang sama muncul dua kali berturut-turut di batas putaran
            if len(self._bag) > 1 and self._bag[-1] == self._last:
                self._bag[0], self._bag[-1] = self._bag[-1], self._bag[0]
        self._last = self._bag.pop()
        return self._last
