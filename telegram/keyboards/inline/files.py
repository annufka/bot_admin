from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async, async_to_sync

from telegram.utils.db_api.db_commands import get_files

@sync_to_async
def all_filtered_files(user_id, category, name):
    all_filtered_files = InlineKeyboardMarkup(row_width=1)
    for item in get_files(user_id, category, name):
        btn = InlineKeyboardButton(text=item['file'].split("/")[1], callback_data='file#'+ str(item['file']))
        all_filtered_files.insert(btn)
    return all_filtered_files