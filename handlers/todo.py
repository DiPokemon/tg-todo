import uuid
from datetime import datetime, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.validators import TodoItem
from database.storage import ensure_chat, load_data, save_data
from keyboards.inline import todo_item_keyboard
from utils.constants import MAX_ITEMS_PER_LIST
from utils.formatters import format_todo_item
from utils.navigation import push as nav_push

router = Router()


@router.message(Command("todo"))
async def todo_command(message: Message) -> None:
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await message.answer("Доступные команды: /todo add &lt;текст&gt;, /todo list", parse_mode="HTML")
        return

    subcommand = args[1].lower()

    if subcommand == "add":
        if len(args) < 3 or not args[2].strip():
            await message.answer("Используйте: /todo add &lt;текст задачи&gt;", parse_mode="HTML")
            return
        await _todo_add(message, args[2].strip())

    elif subcommand == "list":
        await _todo_list(message)

    else:
        await message.answer("Доступные команды: /todo add &lt;текст&gt;, /todo list", parse_mode="HTML")


async def _todo_add(message: Message, text: str) -> None:
    try:
        todo = TodoItem(
            id=str(uuid.uuid4()),
            text=text,
            user_id=message.from_user.id,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        await message.answer(f"Ошибка валидации: {e}")
        return

    data = await load_data()
    chat_id = str(message.chat.id)
    ensure_chat(data, chat_id)

    todos = data["chats"][chat_id]["todo"]
    if len(todos) >= MAX_ITEMS_PER_LIST:
        await message.answer(f"Список задач заполнен (максимум {MAX_ITEMS_PER_LIST}). Удалите часть задач.")
        return

    todos.append(todo.model_dump())
    await save_data(data)
    await message.answer(f"✅ Задача добавлена: {todo.text}")


async def _todo_list(message: Message) -> None:
    data = await load_data()
    chat_id = str(message.chat.id)
    # push navigation state
    nav_push(chat_id, "todo_list")
    todos = data.get("chats", {}).get(chat_id, {}).get("todo", [])

    if not todos:
        await message.answer("Список задач пуст.")
        return

    await message.answer(f"📋 <b>Задачи ({len(todos)}):</b>", parse_mode="HTML")
    for item in todos:
        text = format_todo_item(item)
        await message.answer(text, reply_markup=todo_item_keyboard(item["id"]))

    # add Back button
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")]
    ])
    await message.answer("", reply_markup=back_kb)
