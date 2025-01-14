import logging

from aiogram import executor

from loader import dp, db, telethon_client, pyrogram_client
import middlewares, filters, handlers
from utils.logger import setup_logger
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.create_table_chats()
    await telethon_client.start()
    await pyrogram_client.start()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)



async def on_shutdown(dispatcher):
    await telethon_client.disconnect()
    # await pyrogram_client.stop()


if __name__ == '__main__':

    # my_logger.debug("Bu debug xabari")
    # my_logger.info("Bu info xabari")
    # my_logger.warning("Bu warning xabari")
    # my_logger.error("Bu error xabari")
    # my_logger.critical("Bu critical xabari")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

