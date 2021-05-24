from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from telegram.filters.admin import IsAdmin
from telegram.loader import dp


# start для админа
from telegram.utils.misc import rate_limit


@rate_limit(5, 'start')
@dp.message_handler(CommandStart(), IsAdmin())
async def admin_hello(message: types.Message):
    await message.answer("Привет, админ! Все комманды доступны ниже в меню комманд. Ты можешь добавить пользователя и "
                         "его права, добавить файлы и папку, а также удалить пользователя, папку с файлами")


# start для обычного пользователя
@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\nДля того, чтобы получить справочную '
                         f'информацию нажмите /help.')
    await message.answer(f'Если же Вы хотите перейти к поиску, то нажмите /verificate. '
                         f'Верификация происходит при помощи электронной почты один раз, на которую прийдет '
                         f'сгенерированный код. Вставьте код с почты в бота, после успешной проверки ботом '
                         f'Вы сможете начать поиск файлов.')
