from aiogram.fsm.state import State, StatesGroup


class EditTodoState(StatesGroup):
    waiting_for_text = State()


class EditShopState(StatesGroup):
    waiting_for_text = State()
