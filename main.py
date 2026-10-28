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
