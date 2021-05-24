import re

from aiogram import types

from aiogram.dispatcher.filters import BoundFilter


class IsEmail(BoundFilter):
    async def check(self, message: types.Message):
        pattern = r'^((([0-9A-Za-z]{1}[-0-9A-z\.]{1,}[0-9A-Za-z]{1})|([0-9А-Яа-я]{1}[-0-9А-я\.]{1,}[0-9А-Яа-я]{1}))@([-A-Za-z]{1,}\.){1,2}[-A-Za-z]{2,})'
        return re.match(pattern, message.text)
