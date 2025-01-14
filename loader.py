import logging

from aiogram import Bot, Dispatcher, types
from telethon import TelegramClient
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.postgresql import Database
from utils.logger import setup_logger

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
telethon_client = TelegramClient('userbot', config.API_ID, config.API_HASH)
# pyrogram_client = Client("userbotpyrogram", api_id=API_ID, api_hash=API_HASH)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

my_logger = setup_logger("my_app_logger", "app.log", logging.DEBUG)
