from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.storage import load_data, save_data
from handlers.states import EditShopState, EditTodoState
from keyboards.inline import shopping_item_keyboard, todo_item_keyboard
from utils.constants import MAX_TEXT_LENGTH
from utils.formatters import format_shop_item, format_todo_item
from keyboards.reply import MAIN_MENU
from utils.navigation import pop as nav_pop, current as nav_current

router = Router()


# ─── TODO: done ───────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("todo_done:"))
async def todo_done_callback(call: CallbackQuery) -> None:
    item_id = call.data.split(":", 1)[1]
    data = await load_data()
    chat_id = str(call.message.chat.id)
    todos = data.get("chats", {}).get(chat_id, {}).get("todo", [])

    for item in todos:
        if item["id"] == item_id:
            item["status"] = "completed"
            await save_data(data)
            await call.message.edit_text(
                format_todo_item(item),
                reply_markup=todo_item_keyboard(item_id),
            )
            await call.answer("Отмечено как выполнено ✅")
            return

    await call.answer("Задача не найдена", show_alert=True)


# ─── TODO: edit ───────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("todo_edit:"))
async def todo_edit_callback(call: CallbackQuery, state: FSMContext) -> None:
    item_id = call.data.split(":", 1)[1]
    await state.set_state(EditTodoState.waiting_for_text)
    await state.update_data(item_id=item_id)
    await call.message.edit_text(
        call.message.text + "\n\n✏️ Введите новый текст (или /cancel для отмены):",
        reply_markup=None,
    )
    await call.answer()


@router.message(EditTodoState.waiting_for_text)
async def todo_edit_text_received(message: Message, state: FSMContext) -> None:
    new_text = message.text.strip() if message.text else ""

    if not new_text:
        await message.answer("Текст не может быть пустым. Попробуйте снова или /cancel для отмены.")
        return

    if len(new_text) > MAX_TEXT_LENGTH:
        await message.answer(f"Текст слишком длинный (максимум {MAX_TEXT_LENGTH} символов). Попробуйте снова.")
        return

    state_data = await state.get_data()
    item_id = state_data.get("item_id")

    data = await load_data()
    chat_id = str(message.chat.id)
    todos = data.get("chats", {}).get(chat_id, {}).get("todo", [])

    for item in todos:
        if item["id"] == item_id:
            item["text"] = new_text
            await save_data(data)
            await state.clear()
            await message.answer(f"✅ Задача обновлена: {new_text}")
            return

    await state.clear()
    await message.answer("Задача не найдена.")


# ─── TODO: delete ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("todo_delete:"))
async def todo_delete_callback(call: CallbackQuery) -> None:
    item_id = call.data.split(":", 1)[1]
    data = await load_data()
    chat_id = str(call.message.chat.id)
    chat_data = data.get("chats", {}).get(chat_id)

    if chat_data is None:
        await call.answer("Данные не найдены", show_alert=True)
        return

    todos = chat_data.get("todo", [])
    new_todos = [item for item in todos if item["id"] != item_id]

    if len(new_todos) == len(todos):
        await call.answer("Задача не найдена", show_alert=True)
        return

    chat_data["todo"] = new_todos
    await save_data(data)
    await call.message.edit_text("❌ Задача удалена")
    await call.answer("Удалено")


# ─── SHOP: bought ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("shop_bought:"))
async def shop_bought_callback(call: CallbackQuery) -> None:
    item_id = call.data.split(":", 1)[1]
    data = await load_data()
    chat_id = str(call.message.chat.id)
    items = data.get("chats", {}).get(chat_id, {}).get("shopping", [])

    for item in items:
        if item["id"] == item_id:
            item["status"] = "bought"
            await save_data(data)
            await call.message.edit_text(
                format_shop_item(item),
                reply_markup=shopping_item_keyboard(item_id),
            )
            await call.answer("Отмечено как куплено 🛒")
            return

    await call.answer("Товар не найден", show_alert=True)


# ─── SHOP: edit ───────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("shop_edit:"))
async def shop_edit_callback(call: CallbackQuery, state: FSMContext) -> None:
    item_id = call.data.split(":", 1)[1]
    await state.set_state(EditShopState.waiting_for_text)
    await state.update_data(item_id=item_id)
    await call.message.edit_text(
        call.message.text + "\n\n✏️ Введите новое название (или /cancel для отмены):",
        reply_markup=None,
    )
    await call.answer()


@router.message(EditShopState.waiting_for_text)
async def shop_edit_text_received(message: Message, state: FSMContext) -> None:
    new_text = message.text.strip() if message.text else ""

    if not new_text:
        await message.answer("Текст не может быть пустым. Попробуйте снова или /cancel для отмены.")
        return

    if len(new_text) > MAX_TEXT_LENGTH:
        await message.answer(f"Текст слишком длинный (максимум {MAX_TEXT_LENGTH} символов). Попробуйте снова.")
        return

    state_data = await state.get_data()
    item_id = state_data.get("item_id")

    data = await load_data()
    chat_id = str(message.chat.id)
    items = data.get("chats", {}).get(chat_id, {}).get("shopping", [])

    for item in items:
        if item["id"] == item_id:
            item["text"] = new_text
            await save_data(data)
            await state.clear()
            await message.answer(f"🛒 Товар обновлён: {new_text}")
            return

    await state.clear()
    await message.answer("Товар не найден.")


# ─── SHOP: delete ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("shop_delete:"))
async def shop_delete_callback(call: CallbackQuery) -> None:
    item_id = call.data.split(":", 1)[1]
    data = await load_data()
    chat_id = str(call.message.chat.id)
    chat_data = data.get("chats", {}).get(chat_id)

    if chat_data is None:
        await call.answer("Данные не найдены", show_alert=True)
        return

    items = chat_data.get("shopping", [])
    new_items = [item for item in items if item["id"] != item_id]

    if len(new_items) == len(items):
        await call.answer("Товар не найден", show_alert=True)
        return

    chat_data["shopping"] = new_items
    await save_data(data)
    await call.message.edit_text("❌ Товар удалён")
    await call.answer("Удалено")


# ─── Navigation: Back button ─────────────────────────────────────────────────


@router.callback_query(F.data == "nav_back")
async def nav_back_callback(call: CallbackQuery) -> None:
    chat_id = str(call.message.chat.id)
    prev = nav_pop(chat_id)
    await call.answer()
    # remove the message with the back button
    try:
        await call.message.delete()
    except Exception:
        pass

    if prev == "todo_list":
        from handlers.todo import _todo_list

        await _todo_list(call.message)
        return

    if prev == "shop_list":
        from handlers.shopping import _shop_list

        await _shop_list(call.message)
        return

    # default: show main menu
    await call.message.answer("Главное меню:", reply_markup=MAIN_MENU)
