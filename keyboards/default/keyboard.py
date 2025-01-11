from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Chat qo'shish"), KeyboardButton("Reklama yuborish"))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_button.add(KeyboardButton("Bekor qilish"))