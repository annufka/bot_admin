from aiogram.dispatcher.filters import BoundFilter

from aiogram import types

from telegram.data import config
from telegram.utils.db_api.db_commands import get_all_admins


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        list_of_admins = await get_all_admins()
        admins = [i['telegram_id'] for i in list_of_admins]
        admins_from_config = config.admins
        if str(message.from_user.id) in admins:
            return True
        elif message.from_user.id in admins_from_config:
            return True
        else:
            return


class NotAdmin(BoundFilter):
    async def check(self, message: types.Message):
        list_of_admins = await get_all_admins()
        admins = [i['telegram_id'] for i in list_of_admins]
        admins_from_config = config.admins
        if str(message.from_user.id) not in admins:
            return True
        elif message.from_user.id in admins_from_config:
            return True
        else:
            return
