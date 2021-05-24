from aiogram.dispatcher.filters.state import StatesGroup, State


class FindFile(StatesGroup):
    name_of_file = State()
    category_of_file = State()