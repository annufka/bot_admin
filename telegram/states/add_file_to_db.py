from aiogram.dispatcher.filters.state import StatesGroup, State


class AddFile(StatesGroup):
    enter_dir_create = State()
    enter_category = State()
    load_file = State()