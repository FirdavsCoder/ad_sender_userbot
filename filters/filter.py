from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        # user_id = int(message.from_user.id)
        # if user_id in ADMINS:
        #     return True
        # else:
        #     return False
        return True