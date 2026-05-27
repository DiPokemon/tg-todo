from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def todo_item_keyboard(item_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Выполнено", callback_data=f"todo_done:{item_id}")],
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"todo_edit:{item_id}")],
            [InlineKeyboardButton(text="❌ Удалить", callback_data=f"todo_delete:{item_id}")],
        ]
    )

def shopping_item_keyboard(item_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Куплено", callback_data=f"shop_bought:{item_id}")],
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"shop_edit:{item_id}")],
            [InlineKeyboardButton(text="❌ Удалить", callback_data=f"shop_delete:{item_id}")],
        ]
    )
