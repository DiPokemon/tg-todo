"""
Flask WSGI webhook server for PythonAnywhere deployment.

Telegram sends POST requests to /webhook; Flask forwards each
update to the aiogram dispatcher synchronously using a shared event loop.
"""
import asyncio

from flask import Flask, abort, request

from app.bot import bot, dp
from aiogram.types import Update
from config import LOG_LEVEL
from utils.logger import setup_logger

logger = setup_logger("webhook", LOG_LEVEL)

app = Flask(__name__)

# One event loop for the lifetime of this WSGI worker
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.content_type != "application/json":
        abort(400)

    data = request.get_json(silent=True)
    if data is None:
        abort(400)

    update = Update(**data)
    _loop.run_until_complete(dp.feed_update(bot=bot, update=update))
    return "OK"


@app.route("/", methods=["GET"])
def healthcheck():
    return "Bot is running", 200
