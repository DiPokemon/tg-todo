"""
Register or remove the Telegram webhook. Uses requests (no aiohttp).

Usage:
    python set_webhook.py https://YOUR_USERNAME.pythonanywhere.com/webhook
    python set_webhook.py --delete
    python set_webhook.py --info

You can also open the URL directly in any browser (no proxy needed):
    https://api.telegram.org/bot<TOKEN>/setWebhook?url=<WEBHOOK_URL>
"""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL", "")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN is not set in .env")
    sys.exit(1)

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None


def api(method: str, **params) -> dict:
    url = f"{API_BASE}/{method}"
    resp = requests.post(url, json=params, proxies=PROXIES, timeout=15)
    resp.raise_for_status()
    return resp.json()


def set_webhook(webhook_url: str) -> None:
    result = api("setWebhook", url=webhook_url)
    if result.get("ok"):
        print(f"Webhook set: {webhook_url}")
    else:
        print(f"Error: {result}")
        return
    info = api("getWebhookInfo")["result"]
    print(f"Confirmed URL : {info['url']}")
    print(f"Pending updates: {info.get('pending_update_count', 0)}")
    if info.get("last_error_message"):
        print(f"Last error    : {info['last_error_message']}")


def delete_webhook() -> None:
    result = api("deleteWebhook")
    if result.get("ok"):
        print("Webhook deleted. Bot is now in polling mode.")
    else:
        print(f"Error: {result}")


def show_info() -> None:
    info = api("getWebhookInfo")["result"]
    print(f"URL           : {info.get('url') or '(not set)'}")
    print(f"Pending updates: {info.get('pending_update_count', 0)}")
    if info.get("last_error_message"):
        print(f"Last error    : {info['last_error_message']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--delete":
        delete_webhook()
    elif arg == "--info":
        show_info()
    else:
        set_webhook(arg)
