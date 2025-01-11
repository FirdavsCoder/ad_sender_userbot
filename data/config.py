from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = [1849953640]  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

API_ID = env.int("API_ID")
API_HASH = env.str("API_HASH")


DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASS,
    "database": DB_NAME,
    "host": DB_HOST,
}