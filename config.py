import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
POLLING_TIMEOUT = int(os.getenv("POLLING_TIMEOUT", 30))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
