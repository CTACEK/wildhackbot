from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
from config import adminpass
from dispatcher import dp
import keyboards
from handlers import personal_actions


class FMSAdmin(StatesGroup):
    temppass = State()
    connectionpass = State()

@dp.message_handler(commands="admin", state=None)
async def iwanttobeadmin(message: types.Message):
    await message.answer(f"Введите пароль от админа:")
    await FMSAdmin.temppass.set()


@dp.message_handler(state=FMSAdmin.temppass)
async def checkadmin(message: types.Message, state: FSMContext):
    if message.text == adminpass:
        await message.answer(f"Здравствуйте великий админ {message.from_user.first_name}")
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # buttons = ["Список неотмеченных анкет", "Все анкеты", "Назад"]
        # keyboard.add(*buttons)
        await message.answer((f"*появление интерфеса*"), reply_markup=keyboards.keyboardadmin())
        await FMSAdmin.next()


@dp.message_handler(lambda message: message.text == "Список неотмеченных анкет", state=FMSAdmin.connectionpass)
async def list(message: types.Message):
    await message.answer("Неответ")


@dp.message_handler(lambda message: message.text == "Все анкеты", state=FMSAdmin.connectionpass)
async def list(message: types.Message):
    global admin
    await message.answer("Список волонтёров:")
    result = BotDB.get_bd()
    k = 1
    for person in result:
        if person[3] is not None:
            await message.answer(f"{str(k)} {person[3]}")
            k += 1

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Хотите кого-то найти?", "Назад"]
    keyboard.add(*buttons)
    await message.answer((f"*ожидаю ваше сообщение*"), reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Хотите кого-то найти?", state=FMSAdmin.connectionpass)
async def list(message: types.Message):
    global admin
    await message.answer("Список волонтёров:")
    result = BotDB.get_bd()
    k = 1
    for person in result:
        if person[3] is not None:
            await message.answer(f"{str(k)} {person[3]}")
            k += 1

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Хотите кого-то найти?", "Назад"]
    keyboard.add(*buttons)
    await message.answer((f"*ожидаю ваше сообщение*"), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Назад", state=FMSAdmin.connectionpass)
async def list(message: types.Message, state: FSMContext):
    await message.answer("Вы в режиме юзера")
    await state.finish()
    await personal_actions.start(message)