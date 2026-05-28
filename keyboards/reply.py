from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Задачи"),
            KeyboardButton(text="🛒 Покупки"),
        ],
        [
            KeyboardButton(text="➕ Добавить задачу"),
            KeyboardButton(text="🛍️ Добавить покупку"),
        ],
        [
            KeyboardButton(text="❓ Помощь"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)
