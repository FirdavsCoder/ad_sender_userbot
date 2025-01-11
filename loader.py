from aiogram import Bot, Dispatcher, types
from telethon import TelegramClient
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.postgresql import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
telethon_client = TelegramClient('userbot', config.API_ID, config.API_HASH)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
