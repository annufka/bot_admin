from aiogram.dispatcher.filters.state import StatesGroup, State


class AddUser(StatesGroup):
    enter_email = State()
    enter_dir = State()