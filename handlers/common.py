from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "📋 <b>Доступные команды:</b>\n\n"
        "<b>Задачи:</b>\n"
        "  /todo add &lt;текст&gt; — добавить задачу\n"
        "  /todo list — список задач\n\n"
        "<b>Покупки:</b>\n"
        "  /shop add &lt;товар&gt; — добавить товар\n"
        "  /shop list — список покупок\n\n"
        "<b>Прочее:</b>\n"
        "  /start — информация о боте\n"
        "  /help — эта справка\n"
        "  /cancel — отменить текущее действие",
        parse_mode="HTML",
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять.")
        return
    await state.clear()
    await message.answer("❌ Действие отменено.")
