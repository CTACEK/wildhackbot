from tkinter import Text

from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



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


@dp.message_handler(lambda message: message.text == "FAQ")
async def without_puree(message: types.Message):
    await message.answer("Факью")


@dp.message_handler(lambda message: message.text == "О заповеднике")
async def without_puree(message: types.Message):
    await message.answer("Бла бла бла")



# Заполнение анкеты

class FSMAnket(StatesGroup):
    columns = {"user_id": State(), "full_name": State(), "date_of_application": State(), "mail": State(),
               "birthday": State(), "phone_number": State(), "education": State(), "territory": State(),
               "arrival_date": State(), "departure_date": State(), "lang": State(), "experience": State(),
               "skills": State(), "recommendations": State(), "volunteer_book": State(), "pitch": State(),
               "video": State(), "reviewed": State()}


# Начало диалога
@dp.message_handler(lambda message: message.text == "Заполнить заявку", state=None)
async def cm_start(message: types.Message):
    await FSMAnket.columns.get("full_name").set()
    await message.answer("Введите ФИО")


# Грузим ФИО
@dp.message_handler(state=FSMAnket.columns.get("full_name"))
async def load_fio(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "full_name", message.text)
    await FSMAnket.next()
    await message.answer("Введите почту")


# Ловим второй ответ - почту
@dp.message_handler(state=FSMAnket.columns.get("mail"))
async def load_mail(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "mail", message.text)
    await FSMAnket.next()
    await message.answer("B")

@dp.message_handler(state=FSMAnket.columns.get("mail"))
async def load_mail(message: types.Message, state: FSMContext):
    # загрузка в БД

    await FSMAnket.next()
    await message.answer("Введите чото-там")


