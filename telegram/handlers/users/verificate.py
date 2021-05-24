from aiogram import types
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import string
import random

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ChatActions

from telegram.filters.email import IsEmail
from telegram.filters.isverificate import NotVerificate, IsVerificate
from telegram.loader import dp, bot
from telegram.utils.db_api.db_commands import *

from telegram.utils.misc import rate_limit


# комманда verificate
@rate_limit(5, 'verificate')
@dp.message_handler(Command("verificate"), NotVerificate())
async def bot_start(message: types.Message):
    await message.answer(
        "Для того чтобы найти нужный Вам файл, надо сначала пройти проверку. Для начала введите свою почту.")


@dp.message_handler(Command("verificate"), IsVerificate())
async def bot_start(message: types.Message):
    await message.answer(
        "Вы уже были верифицированы! Вы можете пользоваться поиском")


# генератор случайного кода
def generator(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


# функция для отправления кода на почту
async def send_mail(text, id):
    # объект для письма
    msg = MIMEMultipart()
    # генерируем код для верификации
    code = generator()
    try:
        await update_user_code(code, id)
    except:
        pass
    message = 'Скопируйте все символы со следующей строчки:\nCode' + code
    # параметры сообщения
    password = "" # пароль с почты
    msg['From'] = "" # электронная почта
    msg['To'] = text
    msg['Subject'] = "Код верификации"
    # добавляем тело
    msg.attach(MIMEText(message, 'plain'))
    # создаем сервер
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # логин
    server.login(msg['From'], password)
    # отправляем письмо
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


# если пользователь прислал адресс почты
@dp.message_handler(IsEmail())
async def mail(message: types.Message):
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    try:
        await update_user_telegram_id(message.text, message.from_user.id)
        await send_mail(message.text, message.from_user.id)
        await message.answer("Проверьте свою почту, я прислал Вам код для верификации.")
    except:
        await message.answer("Что-то пошло не так, попробуйте позже.")


@dp.message_handler(Text(startswith='Code'))
async def check_code(message: types.Message):
    code = message.text.replace("Code", "")
    try:
        code_from_db = await get_code(message.from_user.id)
        if code == str(code_from_db):
            await message.answer("Теперь Вы можете пользоваться поиском. Нажмите /find для работы с поиском")
        else:
            await message.answer("Вы ввели неправильный код, попробуйте ещё раз!")
    except:
        pass
