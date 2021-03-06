from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from telegram.loader import dp
from telegram.utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/find -  Поиск файла'
    ]
    await message.answer('\n'.join(text))
