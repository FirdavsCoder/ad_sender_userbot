from aiogram import Bot, Dispatcher, types
from pyrogram import Client
from telethon import TelegramClient
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from data.config import API_ID, API_HASH
from utils.db_api.postgresql import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
telethon_client = TelegramClient('userbot', config.API_ID, config.API_HASH)
pyrogram_client = Client("userbotpyrogram", api_id=API_ID, api_hash=API_HASH)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
