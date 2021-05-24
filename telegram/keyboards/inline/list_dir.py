from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram.utils.db_api.db_commands import get_all_dir_from_db

all_dir = InlineKeyboardMarkup(row_width=1)
for item in get_all_dir_from_db():
    btn = InlineKeyboardButton(text=item.name_of_directory, callback_data='dir#'+ str(item.name_of_directory))
    all_dir.insert(btn)

all_dir_for_file = InlineKeyboardMarkup(row_width=1)
for item in get_all_dir_from_db():
    btn = InlineKeyboardButton(text=item.name_of_directory, callback_data='createfiledir#'+ str(item.name_of_directory))
    all_dir_for_file.insert(btn)