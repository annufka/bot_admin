from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from telegram.keyboards.inline.directories import choice

from telegram.filters.isverificate import IsVerificate
from telegram.keyboards.inline.files import all_filtered_files
from telegram.loader import dp
from telegram.states.find_file import FindFile


from telegram.utils.misc import rate_limit

# find
@rate_limit(5, 'find')
@dp.message_handler(Command("find"), IsVerificate(), state=None)
async def bot_find(message: types.Message):
    await FindFile.name_of_file.set()
    await message.answer("Введите поисковую фразу")


# Поиск (тип файла)
@dp.message_handler(state=FindFile.name_of_file)
async def enter_name_file(message: types.Message, state: FSMContext):
    await state.update_data(name_of_file=message.text)
    await FindFile.next()
    await message.answer("Выберите тип файла", reply_markup=choice)


# поиск по файлу с клавиатуры
@dp.callback_query_handler(lambda call: 'find' in call.data, state=FindFile.category_of_file)
async def enter_category(call, state: FSMContext):
    data = await state.get_data()
    kb_files = await all_filtered_files(call.from_user.id, call.data.split("#")[1], data.get('name_of_file'))
    await call.message.answer("Выберите файл", reply_markup=kb_files)
    await state.finish()


# загрузка файла в чат
@dp.callback_query_handler(lambda call: 'file' in call.data)
async def send_file_from_db(call):
    file = call.data.split("#")[1]
    with open(file, 'rb') as file:
        await dp.bot.send_document(chat_id=call.from_user.id, document=file)
