from aiogram import Dispatcher

from telegram.filters.admin import IsAdmin
from telegram.filters.email import IsEmail


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsEmail)
    dp.filters_factory.bind(IsAdmin)