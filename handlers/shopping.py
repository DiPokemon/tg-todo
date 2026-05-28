import uuid
from datetime import datetime, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.validators import ShoppingItem
from database.storage import ensure_chat, load_data, save_data
from keyboards.inline import shopping_item_keyboard
from utils.constants import MAX_ITEMS_PER_LIST
from utils.formatters import format_shop_item
from utils.navigation import push as nav_push

router = Router()


@router.message(Command("shop"))
async def shop_command(message: Message) -> None:
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await message.answer("Доступные команды: /shop add &lt;товар&gt;, /shop list", parse_mode="HTML")
        return

    subcommand = args[1].lower()

    if subcommand == "add":
        if len(args) < 3 or not args[2].strip():
            await message.answer("Используйте: /shop add <товар> [| дедлайн] [| стоимость]\nПример: /shop add Молоко | 2026-06-01 | 89.99", parse_mode="HTML")
            return
        await _shop_add(message, args[2].strip())

    elif subcommand == "list":
        await _shop_list(message)

    else:
        await message.answer("Доступные команды: /shop add &lt;товар&gt;, /shop list", parse_mode="HTML")


async def _shop_add(message: Message, text: str) -> None:
    try:
        # parse optional fields: text | deadline | cost
        parts = [p.strip() for p in text.split("|")]
        text_only = parts[0]
        deadline = parts[1] if len(parts) > 1 and parts[1] else None
        cost = None
        if len(parts) > 2 and parts[2]:
            try:
                cost = float(parts[2].replace(',', '.'))
            except Exception:
                await message.answer("Неверный формат стоимости. Используйте число, например: 89.99")
                return

        item = ShoppingItem(
            id=str(uuid.uuid4()),
            text=text_only,
            user_id=message.from_user.id,
            created_at=datetime.now(timezone.utc).isoformat(),
            deadline=deadline,
            cost=cost,
        )
    except Exception as e:
        await message.answer(f"Ошибка валидации: {e}")
        return

    data = await load_data()
    chat_id = str(message.chat.id)
    ensure_chat(data, chat_id)

    shopping = data["chats"][chat_id]["shopping"]
    if len(shopping) >= MAX_ITEMS_PER_LIST:
        await message.answer(f"Список покупок заполнен (максимум {MAX_ITEMS_PER_LIST}). Удалите часть товаров.")
        return

    shopping.append(item.model_dump())
    await save_data(data)
    await message.answer(f"🛒 Товар добавлен: {item.text}")


async def _shop_list(message: Message) -> None:
    data = await load_data()
    chat_id = str(message.chat.id)
    # push navigation state
    nav_push(chat_id, "shop_list")
    items = data.get("chats", {}).get(chat_id, {}).get("shopping", [])

    if not items:
        await message.answer("Список покупок пуст.")
        return

    await message.answer(f"🛒 <b>Покупки ({len(items)}):</b>", parse_mode="HTML")
    for item in items:
        text = format_shop_item(item)
        await message.answer(text, reply_markup=shopping_item_keyboard(item["id"]))

    # add Back button
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="nav_back")]
    ])
    await message.answer("", reply_markup=back_kb)
