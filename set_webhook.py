"""
Run this script once on PythonAnywhere to register the webhook URL with Telegram.

Usage:
    python set_webhook.py https://YOUR_USERNAME.pythonanywhere.com/webhook

To remove the webhook (switch back to polling):
    python set_webhook.py --delete
"""
import asyncio
import sys

from aiogram import Bot
from config import BOT_TOKEN


async def set_webhook(url: str) -> None:
    bot = Bot(token=BOT_TOKEN)
    await bot.set_webhook(url)
    info = await bot.get_webhook_info()
    print(f"Webhook set: {info.url}")
    print(f"Pending updates: {info.pending_update_count}")
    await bot.session.close()


async def delete_webhook() -> None:
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook()
    print("Webhook deleted. Bot is now in polling mode.")
    await bot.session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--delete":
        asyncio.run(delete_webhook())
    else:
        asyncio.run(set_webhook(sys.argv[1]))
