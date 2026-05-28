import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from config import BOT_TOKEN, LOG_LEVEL, POLLING_TIMEOUT, PROXY_URL
from handlers import callbacks, common, errors, shopping, todo
from keyboards.reply import MAIN_MENU
from utils.navigation import reset as nav_reset
from utils.logger import setup_logger

logger = setup_logger("bot", LOG_LEVEL)

_session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
bot = Bot(token=BOT_TOKEN, session=_session)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(errors.router)
dp.include_router(common.router)
dp.include_router(todo.router)
dp.include_router(shopping.router)
dp.include_router(callbacks.router)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    # reset navigation stack for this chat
    nav_reset(str(message.chat.id))

    await message.answer(
        "👋 <b>Привет! Я TODO/Shopping бот.</b>\n\n"
        "Помогу вести списки задач и покупок прямо в этом чате.\n\n"
        "Используй кнопки ниже или команды:\n"
        "  📋 <b>Задачи</b> — показать список задач\n"
        "  🛒 <b>Покупки</b> — показать список покупок\n"
        "  ➕ — добавить задачу (введи текст после нажатия)\n"
        "  🛍️ — добавить покупку (введи текст после нажатия)",
        parse_mode="HTML",
        reply_markup=MAIN_MENU,
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
