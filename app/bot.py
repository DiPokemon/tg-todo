import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from config import BOT_TOKEN, LOG_LEVEL, POLLING_TIMEOUT
from handlers import callbacks, common, errors, shopping, todo
from utils.logger import setup_logger

logger = setup_logger("bot", LOG_LEVEL)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(errors.router)
dp.include_router(common.router)
dp.include_router(todo.router)
dp.include_router(shopping.router)
dp.include_router(callbacks.router)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 <b>Привет! Я TODO/Shopping бот.</b>\n\n"
        "Помогу вести списки задач и покупок прямо в этом чате.\n\n"
        "Введите /help для списка команд.",
        parse_mode="HTML",
    )


def start_bot() -> None:
    logger.info("Starting bot...")
    asyncio.run(_run_polling())


async def _run_polling() -> None:
    logger.info("Polling started")
    try:
        await dp.start_polling(bot, polling_timeout=POLLING_TIMEOUT)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")
