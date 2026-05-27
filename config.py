import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
POLLING_TIMEOUT = int(os.getenv("POLLING_TIMEOUT", 30))

# Proxy for outbound HTTP requests (PythonAnywhere free tier).
# Priority: explicit PROXY_URL in .env → system http_proxy env var → empty (no proxy)
PROXY_URL = (
    os.getenv("PROXY_URL")
    or os.getenv("http_proxy")
    or os.getenv("HTTP_PROXY")
    or ""
)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
