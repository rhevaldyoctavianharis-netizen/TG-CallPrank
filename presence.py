"""Status online/offline akun."""
import logging

from telethon import TelegramClient, functions

log = logging.getLogger(__name__)


async def set_online(client: TelegramClient) -> None:
    try:
        await client(functions.account.UpdateStatusRequest(offline=False))
    except Exception as e:
        log.debug("set_online gagal: %s", e)


async def set_offline(client: TelegramClient) -> None:
    try:
        await client(functions.account.UpdateStatusRequest(offline=True))
    except Exception as e:
        log.debug("set_offline gagal: %s", e)
