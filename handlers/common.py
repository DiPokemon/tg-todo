from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.states import AddShopState, AddTodoState
from handlers.todo import _todo_add, _todo_list
from handlers.shopping import _shop_add, _shop_list
from keyboards.reply import MAIN_MENU

router = Router()


@router.message(Command("help"))
@router.message(F.text == "❓ Помощь")
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
        reply_markup=MAIN_MENU,
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять.", reply_markup=MAIN_MENU)
        return
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=MAIN_MENU)


# ─── Reply keyboard buttons ───────────────────────────────────────────────────

@router.message(F.text == "📋 Задачи")
async def btn_todo_list(message: Message) -> None:
    await _todo_list(message)


@router.message(F.text == "🛒 Покупки")
async def btn_shop_list(message: Message) -> None:
    await _shop_list(message)


@router.message(F.text == "➕ Добавить задачу")
async def btn_add_todo(message: Message, state: FSMContext) -> None:
    await state.set_state(AddTodoState.waiting_for_text)
    await message.answer("Введите текст задачи (или /cancel для отмены):")


@router.message(F.text == "🛍️ Добавить покупку")
async def btn_add_shop(message: Message, state: FSMContext) -> None:
    await state.set_state(AddShopState.waiting_for_text)
    await message.answer("Введите название товара (или /cancel для отмены):")


@router.message(AddTodoState.waiting_for_text)
async def add_todo_text_received(message: Message, state: FSMContext) -> None:
    text = message.text.strip() if message.text else ""
    if not text:
        await message.answer("Текст не может быть пустым. Попробуйте снова или /cancel.")
        return
    await state.clear()
    await _todo_add(message, text)


@router.message(AddShopState.waiting_for_text)
async def add_shop_text_received(message: Message, state: FSMContext) -> None:
    text = message.text.strip() if message.text else ""
    if not text:
        await message.answer("Текст не может быть пустым. Попробуйте снова или /cancel.")
        return
    await state.clear()
    await _shop_add(message, text)
