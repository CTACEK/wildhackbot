from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


def keyboardadmin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Список неотмеченных анкет", "Все анкеты", "На главное меню"]
    keyboard.add(*buttons)

def keyboardadmin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Список неотмеченных анкет", "Все анкеты", "На главное меню"]
    keyboard.add(*buttons)
