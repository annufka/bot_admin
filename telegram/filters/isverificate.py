from aiogram import types

from aiogram.dispatcher.filters import BoundFilter

from telegram.utils.db_api.db_commands import get_user_by_id


class NotVerificate(BoundFilter):

    async def check(self, message: types.Message):
        user = await get_user_by_id(message.from_user.id)
        return True if not user else False


class IsVerificate(BoundFilter):

    async def check(self, message: types.Message):
        user = await get_user_by_id(message.from_user.id)
        return True if user else False