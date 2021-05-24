from aiogram.dispatcher.filters.state import StatesGroup, State


class AddDir(StatesGroup):
    enter_dir = State()