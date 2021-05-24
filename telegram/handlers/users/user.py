from aiogram import types
from aiogram.dispatcher.filters import Command

from telegram.filters.admin import NotAdmin
from telegram.filters.isverificate import NotVerificate
from telegram.loader import dp

# комманды админа, на которые реши нажать обычный пользователь
@dp.message_handler(Command("add_user"), NotAdmin())
async def bot_start(message: types.Message):
    await message.answer("Ошибка доступа")

@dp.message_handler(Command("add_file"), NotAdmin())
async def bot_start(message: types.Message):
    await message.answer("Ошибка доступа")

@dp.message_handler(Command("add_dir"), NotAdmin())
async def bot_start(message: types.Message):
    await message.answer("Ошибка доступа")

@dp.message_handler(Command("find"), NotVerificate())
async def bot_find_not_verification(message: types.Message):
    await message.answer("Пройдите верификацию /verificate")