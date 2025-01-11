from aiogram import executor

from loader import dp, db, telethon_client
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.create_table_chats()
    await telethon_client.start()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)



async def on_shutdown(dispatcher):
    await telethon_client.disconnect()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
