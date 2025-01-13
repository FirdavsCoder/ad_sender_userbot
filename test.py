from telethon import TelegramClient

# Telegram API ma'lumotlari
# BOT_TOKEN=6530829880:AAGQd7RbXbpb8jiW9894hqBzdhXhWYxxrYk
API_HASH="f86d916561769e47392871db1b97cb4b"
API_ID=12676759

client = TelegramClient('userbot', API_ID, API_HASH)

async def fetch_entity_info():
    try:
        # Bu yerdan kanal, guruh yoki foydalanuvchi haqidagi to'liq ma'lumotni olish mumkin
        entity = await client.get_entity('6286074984')
        print("Entity ma'lumotlari:", entity)
    except Exception as e:
        print(f"Xato yuz berdi: {e}")

with client:
    client.loop.run_until_complete(fetch_entity_info())
