from aiogram import types, Dispatcher

import re
from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
from config import adminpass
from dispatcher import dp
import keyboards

admin = ["Список неотмеченных анкет", "Все анкеты", "Назад"]

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


#
# @dp.message_handler(state=FMSAdmin.connectionpass)
# async def admin(message: types.Message, state: FSMContext):
#     print("z nen")
#     await message.answer(f"Здравствуйте великий админ {message.from_user.first_name}")
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Список неотмеченных анкет", "Все анкеты"]
#     keyboard.add(*buttons)
#     await state.finish()

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
    await start(message)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    bot = Bot(token=config.BOT_TOKEN)
    me = await bot.get_me()

    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id,
                                   (
                                       f"Здравствуйте, {message.from_user.first_name} 👋 Я {me.first_name} помогу ответить на Ваш вопрос. Что Вы хотели бы узнать?"))


    await message.answer((f"*ожидаю ваше сообщение*"), reply_markup=keyboards.keyboarduser())
    # await message.answer((f"Чего желаете, {message.from_user.first_name}?"), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "FAQ")
async def without_puree(message: types.Message):
    await message.answer("Факью")


@dp.message_handler(lambda message: message.text == "О заповеднике")
async def without_puree(message: types.Message):
    await message.answer("Бла бла бла")


# Заполнение анкеты

class FSMAnket(StatesGroup):
    full_name = State()
    mail = State()
    birthday = State()
    phone_number = State()
    education = State()
    territory = State()
    arrival_date = State()
    departure_date = State()
    lang = State()
    experience = State()
    skills = State()
    recommendations = State()
    volunteer_book = State()
    pitch = State()
    video = State()


# Начало диалога
@dp.message_handler(lambda message: message.text == "Заполнить заявку", state=None)
async def cm_start(message: types.Message):
    await FSMAnket.full_name.set()
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = ["Да", "Нет"]
    # keyboard.add(*buttons)
    await message.answer("Для заполнения анкеты напишите свое ФИО 👤", reply_markup=types.ReplyKeyboardRemove())


# Грузим ФИО
@dp.message_handler(state=FSMAnket.full_name)
async def load_fio(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "full_name", message.text)
    await FSMAnket.next()
    await message.answer("Введите Вашу почту 📬")


# Ловим второй ответ - почту
@dp.message_handler(state=FSMAnket.mail)
async def load_mail(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "mail", message.text)
    await FSMAnket.next()
    await message.answer("Укажите Вашу дату рождения 📅", reply_markup=types.ReplyKeyboardRemove())


# Запоминаем дату рождения
@dp.message_handler(state=FSMAnket.birthday)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "birthday", message.text)
    await FSMAnket.next()
    await message.answer("Напишите Ваш номер телефона 📱")


# Номер телефона пользователя
@dp.message_handler(state=FSMAnket.phone_number)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "phone_number", message.text)
    await FSMAnket.next()
    await message.answer("Какое у Вас образование? 🎓")


# Какое образование у юзера
@dp.message_handler(state=FSMAnket.education)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "education", message.text)
    await FSMAnket.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Озерный", "Травяной", "Узон", "Долина гейзеров", "Исток и Аэродром", "Кроноки и Семячик"]
    keyboard.add(*buttons)
    await message.answer(
        "Укажите желаемую территорию для осуществления волонтерских работ 🏞 \n\nПодробнее Вы можете ознакомиться с "
        "территориями Кроноцкого заповедника и Южно-Камчатского заказника, с кордонами, со структурой заповедника, "
        "с актуальными событиями, происходящими на наших территориях на нашем сайте www.kronoki.ru \n\nПодсказка: На "
        "сайте необходимо найти раздел Волонтерство ➝ Волонтерство на территориях ", reply_markup=keyboard)


# Выбор заповедника
@dp.message_handler(
    state=FSMAnket.territory)  # СЮДА ПОТОМ ВКЛИНИТЬ КНОПАЧЬКИ С ВЫБОРОМ ЗАПОВЕДНИКА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "territory", message.text)
    await FSMAnket.next()
    await message.answer("Какую дату заезда Вы планируете? 📆", reply_markup=types.ReplyKeyboardRemove())


# Дата заезда
@dp.message_handler(state=FSMAnket.arrival_date)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "arrival_date", message.text)
    await FSMAnket.next()
    await message.answer("Какую дату выезда Вы планируете? 📆")


# Дата выезда
@dp.message_handler(state=FSMAnket.departure_date)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "departure_date", message.text)
    await FSMAnket.next()
    await message.answer("Какими языками владеете? 🌎")


# Какими языками владеет пользователь
@dp.message_handler(state=FSMAnket.lang)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "lang", message.text)
    await FSMAnket.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Имеется ли у Вас опыт волонтерских работ? 👥", reply_markup=keyboard)


# Опыт работы волонтером
@dp.message_handler(state=FSMAnket.experience)  # КНОПАЧЬКИ ДА/НЕТ!!!!!!!!!!!!!!!!!!!!!!!!!
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "experience", message.text)
    await FSMAnket.next()
    await message.answer("Какими навыками Вы владеете? 👨‍🔧", reply_markup=types.ReplyKeyboardRemove())


# Какими навыками владеет пользователь
@dp.message_handler(state=FSMAnket.skills)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "skills", message.text)
    await FSMAnket.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Есть ли у вас рекомендации? 📄", reply_markup=keyboard)


# Есть ли рекомендации
@dp.message_handler(state=FSMAnket.recommendations)  # КНОПАЧЬКИ ДА/НЕТ!!!!!!!!!!!!!!!!!!!!!!!!!
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "recommendations", message.text)
    await FSMAnket.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Имеется ли у Вас волонтерская книжка? 📖", reply_markup=keyboard)


# Есть ли волонтерская книжка
@dp.message_handler(state=FSMAnket.volunteer_book)  # КНОПАЧЬКИ ДА/НЕТ!!!!!!!!!!!!!!!!!!!!!!!!!
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "volunteer_book", message.text)
    await FSMAnket.next()
    await message.answer("Почему именно Вы должны стать волонтером? 🌟 \n\nРасскажите коротко о себе и своих качествах", reply_markup=types.ReplyKeyboardRemove())


# Почему именно Вы
@dp.message_handler(state=FSMAnket.pitch)
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "pitch", message.text)
    await FSMAnket.next()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Пропустить"]
    keyboard.add(*buttons)
    await message.answer(
        "Для повышения шансов на успешное прохождения отбора Вы можете прикрепить небольшое видео о себе, либо ссылку "
        "на него 🎬 \n\nЭто необязательный шаг, по желанию можете пропустить его", reply_markup=keyboard)


# Видео о себе
@dp.message_handler(state=FSMAnket.video)  # ДОБАВИТЬ ВОЗМОЖНОСТЬ ПРОПУСКА ДАННОГО ШАГА!!!!!!!!!!!!!!!!!
async def load_birthday(message: types.Message, state: FSMContext):
    BotDB.add_information(message.from_user.id, "video", message.text)
    await state.reset_state()
    await message.answer("Если у Вас есть, что добавить к анкете, можете написать это сейчас🙌", reply_markup=types.ReplyKeyboardRemove())

#
# # Добавка к анкете
# @dp.message_handler(state=FSMAnket.reviewed)
# async def load_birthday(message: types.Message, state: FSMContext):
#     BotDB.add_information(message.from_user.id, "reviewed", message.text)
#     await FSMAnket.next()
#     await message.answer("Ваша анкета заполнена, хотите проверить свои основные данные? 👀") #КНОПАЧЬКА ДА/НЕТ ДЛЯ ВОЗМОЖНОСТИ ПРОВЕРКИ ДАННЫХ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#
