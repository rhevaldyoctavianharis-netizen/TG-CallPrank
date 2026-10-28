"""Membuat SESSION_STRING untuk deploy (Heroku). Jalankan sekali di komputer/Termux sendiri."""
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("API_ID   : ").strip())
api_hash = input("API_HASH : ").strip()

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\n=== SESSION_STRING (RAHASIA, jangan dibagikan ke siapa pun) ===\n")
    print(client.session.save())
    print("\n===============================================================")
