from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


def keyboardadmin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Список неотмеченных анкет", "Все анкеты", "Режим пользователя"]
    keyboard.add(*buttons)
    return keyboard

def keyboarduser():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Заполнить заявку", "FAQ", "О заповеднике"]
    keyboard.add(*buttons)
    return keyboard
#