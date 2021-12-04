from tkinter import Text

from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB
from aiogram import Bot
from keyboards import menu


@dp.message_handler(commands="start")
async def start(message: types.Message):

    bot = Bot(token=config.BOT_TOKEN)
    me = await bot.get_me()

    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id,
        (f"Здравствуйте, {message.from_user.first_name} 👋 Я {me.first_name} помогу ответить на Ваш вопрос. Что Вы хотели бы узнать?"))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Заполнить заявку", "FAQ", "О заповеднике"]
    keyboard.add(*buttons)
    await message.answer((f"Чего желаете, {message.from_user.first_name}?"), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Заполнить заявку")
async def without_puree(message: types.Message):

    await message.answer("Для заполнения анкеты напишите свое ФИО")




@dp.message_handler(lambda message: message.text == "FAQ")
async def without_puree(message: types.Message):
    await message.answer("Фак ю")


@dp.message_handler(lambda message: message.text == "О заповеднике")
async def without_puree(message: types.Message):
    await message.answer("Бла бла бла")

