"""Semua pengaturan dibaca dari .env dan dari daftar audio di bawah."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# ---------- Telegram ----------
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_NAME = os.getenv("SESSION_NAME", "prank_session")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# ---------- Audio ----------
# Audio utama: selalu diputar pertama kali saat telepon diangkat
MAIN_AUDIO = ASSETS_DIR / "main.mp3"

# Audio seram/disturbing: SESUAIKAN SENDIRI di sini (nama file di folder assets).
# Kalau list ini dikosongkan, semua file audio di assets (kecuali main.mp3)
# akan dipakai otomatis.
DISTURBING_AUDIOS = [
    "unavailable.mp3",
    "notavailable.mp3",
    # "tawa.mp3",
    # "ketukan.mp3",
]
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".opus", ".flac"}


# ---------- Helper ----------
def _float(name: str, default: float) -> float:
    return float(os.getenv(name, default))


def _ids(name: str) -> set[int]:
    raw = os.getenv(name, "").replace(" ", "")
    return {int(x) for x in raw.split(",") if x}


# ---------- Telepon ----------
MAX_CALL_SECONDS = _float("MAX_CALL_SECONDS", 300)
GAP_MIN = _float("GAP_MIN", 1)
GAP_MAX = _float("GAP_MAX", 4)
ALLOWED_IDS = _ids("ALLOWED_IDS")

# ---------- Chat ----------
CHAT_DELAY_MIN = _float("CHAT_DELAY_MIN", 5)
CHAT_DELAY_MAX = _float("CHAT_DELAY_MAX", 40)
TYPING_MIN = _float("TYPING_MIN", 4)
TYPING_MAX = _float("TYPING_MAX", 12)
BURSTS_MIN = int(_float("BURSTS_MIN", 1))
BURSTS_MAX = int(_float("BURSTS_MAX", 3))
CHAT_COOLDOWN = _float("CHAT_COOLDOWN", 120)
