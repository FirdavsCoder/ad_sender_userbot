from aiogram.dispatcher.filters.state import StatesGroup, State


class AddChat(StatesGroup):
    chat_id = State()

class SendAdState(StatesGroup):
    message = State()