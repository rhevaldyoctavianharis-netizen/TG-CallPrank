"""Entry point: python main.py"""
import asyncio
import logging

from pytgcalls import PyTgCalls, idle
from telethon import TelegramClient
from telethon.sessions import StringSession

import call_handler
import chat_handler
import config
from presence import set_offline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


async def main() -> None:
    config.ASSETS_DIR.mkdir(exist_ok=True)
    if not config.MAIN_AUDIO.exists():
        raise SystemExit(f"File utama tidak ditemukan: {config.MAIN_AUDIO}")

    session = StringSession(config.SESSION_STRING) if config.SESSION_STRING else config.SESSION_NAME
    client = TelegramClient(session, config.API_ID, config.API_HASH)
    call_py = PyTgCalls(client)

    # Cek login dulu: kalau session tidak valid, berhenti dengan pesan jelas (bukan minta nomor HP)
    log.info("SESSION_STRING terisi: %s (panjang %d)", bool(config.SESSION_STRING), len(config.SESSION_STRING))
    await client.connect()
    if not await client.is_user_authorized():
        raise SystemExit(
            "SESSION_STRING kosong/tidak valid/tidak cocok dengan API_ID & API_HASH. "
            "Buat ulang dengan generate_session.py memakai API_ID & API_HASH yang SAMA dengan di Config Vars."
        )

    chat_handler.register(client)
    call_handler.register(call_py)

    await call_py.start()  # juga menjalankan client (login pertama kali minta nomor HP)
    await set_offline(client)
    log.info("Userbot prank aktif. Tekan Ctrl+C untuk berhenti.")
    await idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
