import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ChatActions, ContentType
from django.db import IntegrityError

from telegram.filters import IsEmail, IsAdmin
from telegram.keyboards.inline.directories import choice_for_create
from telegram.keyboards.inline.list_dir import all_dir, all_dir_for_file
from telegram.loader import dp
from aiogram import types

from telegram.states.add_dir_to_db import AddDir
from telegram.states.add_file_to_db import AddFile
from telegram.states.add_user_to_db import AddUser
from telegram.utils.db_api.db_commands import *

from telegram.utils.misc import rate_limit


# кнопки админа
# добавить пользователя
@rate_limit(5, 'add_user')
@dp.message_handler(Command("add_user"), IsAdmin(), state=None)
async def bot_start(message: types.Message):
    await AddUser.enter_email.set()
    await message.answer("Введите email нового пользователя")


# выбор доступа для созлаваемог пользователя
@dp.message_handler(IsEmail(), state=AddUser.enter_email)
async def bot_add_to_bd(message: types.Message, state: FSMContext):
    email = message.text
    try:
        await add_user(email)
        await state.update_data(email=email)
        await AddUser.next()
        await message.answer(f"Выберите папку, которую может просматривать пользователь с email - {email}",
                             reply_markup=all_dir)

    except IntegrityError:
        await message.answer(f"Пользователь с email {email} есть в системе")


# запись пользователя и его доступа в БД
@dp.callback_query_handler(lambda call: 'dir' in call.data, state=AddUser.enter_dir)
async def add_dir_to_user(call, state: FSMContext):
    dir_from_call = call.data.split('#')[1]
    data = await state.get_data()
    try:
        await dp.bot.send_chat_action(call.message.from_user.id, ChatActions.TYPING)
        await add_dir_to_user_in_db(email=data.get("email"), name_dir=dir_from_call)
        await call.message.answer('Готово!')
    except:
        await call.message.answer('Что-то пошло не так, попробуйте через личный кабинет в браузере')
    finally:
        await state.reset_state()


# добавить папку
@rate_limit(5, 'add_dir')
@dp.message_handler(Command("add_dir"), IsAdmin(), state=None)
async def add_directory(message: types.Message):
    await AddDir.enter_dir.set()
    await message.answer("Введите название новой папки")


# добавление папки в БД
@dp.message_handler(IsAdmin(), state=AddDir.enter_dir)
async def add_dir_to_bd(message: types.Message, state: FSMContext):
    name_dir = message.text
    try:
        await add_dir_to_db(name_dir)
        await state.reset_state()
        await message.answer("Готово!")
    except IntegrityError:
        await message.answer("Папка с таким названием уже существует")


# добавить файл
@rate_limit(5, 'add_file')
@dp.message_handler(Command("add_file"), IsAdmin(), state=None)
async def add_directory(message: types.Message):
    await AddFile.enter_dir_create.set()
    await message.answer("Выберите папку для загрузки файла", reply_markup=all_dir_for_file)


# выбрать папку для файла
@dp.callback_query_handler(lambda call: 'createfiledir' in call.data, state=AddFile.enter_dir_create)
async def bot_add_to_bd(call: types.Message, state: FSMContext):
    directory = call.data.split("#")[1]
    await state.update_data(enter_dir_create=directory)
    await AddFile.next()
    await call.message.answer("Выберите категорию", reply_markup=choice_for_create)


# выбрать тип файла
@dp.callback_query_handler(lambda call: 'createcategory' in call.data, state=AddFile.enter_category)
async def add_dir_to_user(call, state: FSMContext):
    category = call.data.split('#')[1]
    await state.update_data(enter_category=category)
    await AddFile.next()
    await call.message.answer("Загрузите файл")


# загрузить файл и все это в БД
@dp.message_handler(content_types=ContentType.DOCUMENT, state=AddFile.load_file)
async def load_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_path = await dp.bot.get_file(message.document.file_id)
    await add_file_to_db(data.get('enter_dir_create'), file_path.file_path, data.get('enter_category'))
    await message.answer("Готово!")

    # try:
    #     await add_dir_to_db(data.get('enter_dir_create'), file, data.get('enter_category'))
    #     await message.answer("Готово!")
    # except IntegrityError:
    #     await message.answer("Файл с таким названием уже существует")
    await state.finish()


# удалить папку
@rate_limit(5, 'delete_dir')
@dp.message_handler(Command("delete_dir"), IsAdmin())
async def add_directory(message: types.Message):
    await message.answer("Выберите папку для загрузки файла", reply_markup=all_dir)

@rate_limit(5, 'cancel')
@dp.message_handler(Command("cancel"), IsAdmin(), state=AddUser.enter_email)
async def add_directory(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Отменено")

@rate_limit(5, 'cancel')
@dp.message_handler(Command("cancel"), IsAdmin(), state=AddDir.enter_dir)
async def add_directory(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Отменено")

@rate_limit(5, 'cancel')
@dp.message_handler(Command("cancel"), IsAdmin(),state=AddFile.enter_dir_create)
async def add_directory(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Отменено")

@rate_limit(5, 'cancel')
@dp.message_handler(Command("cancel"), IsAdmin(),state=AddFile.enter_category)
async def add_directory(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Отменено")

@rate_limit(5, 'cancel')
@dp.message_handler(Command("cancel"), IsAdmin(),state=AddFile.load_file)
async def add_directory(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Отменено")
