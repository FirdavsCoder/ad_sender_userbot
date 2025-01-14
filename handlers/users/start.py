import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import os
from telethon.tl.types import User, Chat, Channel, PeerUser, PeerChannel, PeerChat

from filters.filter import IsAdmin
from keyboards.default.keyboard import main_menu, cancel_button
from loader import dp, db, bot, telethon_client, my_logger
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
    data = await db.select_chat(chat_id=int(chat_id))
    if data:
        await message.answer("Bu chat avval qo'shilgan!", reply_markup=main_menu)
        await state.finish()
        return


    await telethon_client.connect()

    await telethon_client.start()


    try:
        try:
            peer = PeerUser(int(chat_id))
            entity = await telethon_client.get_entity(peer)
            await bot.send_message(chat_id=1849953640, text=f"{entity}")
        except Exception as e:
            my_logger.error(f"ADD CHAT: GET ENTITY USER TELETHON:  (chat_id={chat_id}): {e}")
            try:
                peer = PeerChat(int(chat_id))
                entity = await telethon_client.get_entity(peer)
                await bot.send_message(chat_id=1849953640, text=f"{entity}")
            except Exception as e:
                my_logger.error(f"ADD CHAT: GET ENTITY CHAT TELETHON:  (chat_id={chat_id}): {e}")
                try:
                    peer = PeerChannel(int(chat_id))
                    entity = await telethon_client.get_entity(peer)
                    await bot.send_message(chat_id=1849953640, text=f"{entity}")
                except Exception as e:
                    my_logger.error(f"ADD CHAT: GET ENTITY CHANNEL TELETHON:  (chat_id={chat_id}): {e}")
                    try:
                        chat = await pyrogram_client.get_chat(int(chat_id))
                        await bot.send_message(chat_id=1849953640, text=f"{chat}")
                    except Exception as e:
                        my_logger.error(f"ADD CHAT: GET CHAT TELETHON:  (chat_id={chat_id}): {e}")
        await db.add_chat(chat_id=int(chat_id), type_chat="TEST")
        await message.answer("Chat muvaffaqiyatli qo'shildi!", reply_markup=main_menu)
        await state.finish()
    except Exception as e:
        await message.answer(e)

    try:
        chat = await pyrogram_client.get_chat(chat_id)

        await bot.send_message(chat_id=1849953640, text=f"{chat}")
    except Exception as e:
        await message.answer(e)

    try:
        user = await pyrogram_client.get_users(chat_id)
        await bot.send_message(chat_id=1849953640, text=f"{user}")
    except Exception as e:
        await message.answer(e)



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
                    try:
                        peer = PeerUser(int(chat_id))
                        entity = await telethon_client.get_entity(peer)
                    except Exception as e:
                        my_logger.error(f"GET ENTITY USER TELETHON:  (chat_id={chat_id}): {e}")
                        try:
                            peer = PeerChat(int(chat_id))
                            entity = await telethon_client.get_entity(peer)
                        except Exception as e:
                            my_logger.error(f"GET ENTITY CHAT TELETHON:  (chat_id={chat_id}): {e}")
                            try:
                                peer = PeerChannel(int(chat_id))
                                entity = await telethon_client.get_entity(peer)
                            except Exception as e:
                                my_logger.error(f"GET ENTITY CHANNEL TELETHON:  (chat_id={chat_id}): {e}")
                                try:
                                    chat = await pyrogram_client.get_chat(int(chat_id))
                                except Exception as e:
                                    my_logger.error(f"GET CHAT TELETHON:  (chat_id={chat_id}): {e}")
                except Exception as e:
                    await message.answer(e)

                caption = message.caption or ""

                if message.text:
                    await telethon_client.send_message(entity, message.text)

                else:
                    for media_type, (ext, getter) in MEDIA_TYPES.items():
                        if getattr(message, media_type, None):
                            await download_and_send(chat, message, ext, getter, caption)
                            break
                    else:
                        await message.answer(f"Ushbu xabar turi qo'llab-quvvatlanmaydi: {message.content_type}")
            except Exception as e:
                logging.error(f"Xato yuz berdi (chat_id={chat_id}): {e}")

    await message.answer("Xabar muvaffaqiyatli yuborildi!")
    await state.finish()

