import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import os
from telethon.tl.types import User, Chat, Channel

from filters.filter import IsAdmin
from keyboards.default.keyboard import main_menu, cancel_button
from loader import dp, db, bot, telethon_client
from states.states import AddChat, SendAdState
import logging


@dp.message_handler(IsAdmin(), text="Bekor qilish", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Bekor qilindi!", reply_markup=main_menu)


@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Quyidagi menyudan tanlang:", reply_markup=main_menu)

@dp.message_handler(CommandStart(), state="*")
async def bot_start1(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Xush kelibsiz!")



@dp.message_handler(IsAdmin(),lambda message: message.text == "Chat qo'shish")
async def start_adding_chat(message: types.Message):
    await message.answer("Chat ID ni yuboring:", reply_markup=cancel_button)
    await AddChat.chat_id.set()



@dp.message_handler(IsAdmin(), state=AddChat.chat_id)
async def add_chat(message: types.Message, state: FSMContext):
    chat_id = message.text
    await db.add_chat(chat_id=int(chat_id), type_chat="TEST")
    await message.answer("Chat muvaffaqiyatli qo'shildi!", reply_markup=main_menu)
    await state.finish()
    # try:
    #     if chat_id.isdigit():
    #         chat_id = int(chat_id)
    #     else:
    #         raise ValueError("Chat ID noto'g'ri formatda!")
    #     entity = await telethon_client.get_entity(chat_id)
    #     if isinstance(entity, User):
    #         entity_type = "Foydalanuvchi"
    #         title = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
    #     elif isinstance(entity, Chat):
    #         entity_type = "Oddiy guruh"
    #         title = entity.title
    #     elif isinstance(entity, Channel):
    #         entity_type = "Kanal yoki superguruh"
    #         title = entity.title
    #     else:
    #         entity_type = "Noma'lum tur"
    #         title = "Noma'lum"
    #
    #     await message.answer(
    #         f"Entity topildi!\n\n"
    #         f"Turi: {entity_type}\n"
    #         f"Nomi: {title}\n"
    #         f"ID: {chat_id}"
    #     )
    #
    #     await db.add_chat(chat_id=chat_id, type_chat=entity_type)
    #
    #     await message.answer("Chat muvaffaqiyatli qo'shildi!", reply_markup=main_menu)
    # except ValueError as ve:
    #     await message.answer(f"Noto'g'ri ID: {ve}")
    # except Exception as e:
    #     print(f"Xato yuz berdi: {e}")
    #     await message.answer("Chat topilmadi yoki unga kirish imkoni yo'q.", reply_markup=main_menu)
    #
    # await state.finish()


@dp.message_handler(IsAdmin(), text="Reklama yuborish")
async def send_ad(message: types.Message):
    await message.answer("Yubormoqchi bo'lgan xabaringizni forward qiling:", reply_markup=cancel_button)
    await SendAdState.message.set()


MEDIA_FOLDER = "media"

os.makedirs(MEDIA_FOLDER, exist_ok=True)


MEDIA_TYPES = {
    "photo": ("jpg", lambda msg: msg.photo[-1]),
    "video": ("mp4", lambda msg: msg.video),
    "animation": ("gif", lambda msg: msg.animation),
    "document": (None, lambda msg: msg.document),
    "audio": ("mp3", lambda msg: msg.audio),
    "voice": ("ogg", lambda msg: msg.voice),
    "video_note": ("mp4", lambda msg: msg.video_note),
}

async def download_and_send(entity, message, file_ext, file_getter, caption):
    file = file_getter(message)
    file_path = os.path.join(MEDIA_FOLDER, f"{file.file_unique_id}.{file_ext or file.file_name.split('.')[-1]}")
    await file.download(destination_file=file_path)
    await telethon_client.send_file(entity, file=file_path, caption=caption)
    if os.path.exists(file_path):
        os.remove(file_path)

@dp.message_handler(IsAdmin(), state=SendAdState.message, content_types=types.ContentType.ANY)
async def send_ad(message: types.Message, state: FSMContext):
    chats = await db.select_all_chats()

    async with telethon_client:
        for chat in chats:
            chat_id = chat[0]
            try:
                try:
                    entity = await telethon_client.get_entity(chat_id)
                except Exception as e:
                    logging.error(f"Chatni olishda xato (chat_id={chat_id}): {e}")
                    continue

                caption = message.caption or ""

                if message.text:
                    await telethon_client.send_message(entity, message.text)
                else:
                    for media_type, (ext, getter) in MEDIA_TYPES.items():
                        if getattr(message, media_type, None):
                            await download_and_send(entity, message, ext, getter, caption)
                            break
                    else:
                        await message.answer(f"Ushbu xabar turi qo'llab-quvvatlanmaydi: {message.content_type}")
            except Exception as e:
                logging.error(f"Xato yuz berdi (chat_id={chat_id}): {e}")

    await message.answer("Xabar muvaffaqiyatli yuborildi!")
    await state.finish()

