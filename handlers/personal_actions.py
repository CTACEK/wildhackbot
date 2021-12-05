from aiogram import types, Dispatcher

import re
import requests
from bot import BotDB
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
from config import adminpass
from dispatcher import dp, bot
import keyboards
import searching
from pathlib import Path
from aiogram.types import ContentType, File, Message
from vosk import Model, KaldiRecognizer
import sys
import json
import os
import time
import wave


class FMSAdmin(StatesGroup):
    temppass = State()
    connectionpass = State()
    find_anket = State()
    add_comment = State()


#
#
# #
# async def handle_file(file: File, file_name: str, path: str):
#     Path(f"{path}").mkdir(parents=True, exist_ok=True)
#
#     await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
#


# @dp.message_handler(content_types=[ContentType.VOICE])
# async def voice_message_handler(message: Message):
#     print("aaa")
#     model = Model(r"vosk-model-small-ru-0.22")
#
#     wf = wave.open(r'C:\Users\Яна\PycharmProjects\wildhackbot\232.wav', "rb")
#     rec = KaldiRecognizer(model, 16000)
#
#     result = ''
#     last_n = False
#
#     while True:
#         data = wf.readframes(16000)
#         if len(data) == 0:
#             break
#
#         if rec.AcceptWaveform(data):
#             res = json.loads(rec.Result())
#
#             if res['text'] != '':
#                 result += f" {res['text']}"
#                 last_n = False
#             elif not last_n:
#                 result += '\n'
#                 last_n = True
#
#     res = json.loads(rec.FinalResult())
#     result += f" {res['text']}"
#
#     print(result)


#
#
#

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
    ans = ""
    db = BotDB.get_bd()
    k = 1
    for person in db:
        if person[3] is not None and (person[-1] == None or person[-1] == "Рассмотрение"):
            ans += f"{str(k)}. {person[3]} \n"
            k += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Найти анкету", "Назад"]
    keyboard.add(*buttons)
    await message.answer(ans)
    await message.answer("Найти анкету по ФИО в базе данных?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Все анкеты", state=FMSAdmin.connectionpass)
async def list(message: types.Message, state=FSMContext):
    await message.answer("Список волонтёров:")
    result = BotDB.get_bd()
    ans = ""
    k = 1
    for person in result:
        if person[3] is not None:
            ans += f"{str(k)} {person[3]} \n"
            k += 1
    await message.answer(ans)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Найти анкету", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Найти анкету по ФИО в базе данных?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Назад", state=FMSAdmin.connectionpass)
async def back(message: types.Message):
    await message.answer("Возвращение к меню администратора", reply_markup=keyboards.keyboardadmin())


@dp.message_handler(lambda message: message.text == "Найти анкету", state=FMSAdmin.connectionpass)
async def list(message: types.Message, state: FSMContext):
    await message.answer("Введите полностью ФИО", reply_markup=types.ReplyKeyboardRemove())
    await FMSAdmin.next()


@dp.message_handler(state=FMSAdmin.find_anket)
async def finding(message: types.Message, state: FSMContext):
    answ = ""
    columns = ["id", "user_id", "join_date", "full_name", "date_of_application", "mail", "birthday", "phone_number",
               "education",
               "territory", "arrival_date", "departure_date", "lang", "experience", "skills", "recommendations",
               "volunteer_book", "pitch", "video", "reviewed"]
    db = BotDB.get_bd()
    for row in db:
        if row[3] == message.text:
            await state.update_data(finded=row[1])
            for i in range(len(row)):
                answ += columns[i] + ": " + str(row[i]) + "\n"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Добавить комментарий", "Назад"]
    keyboard.add(*buttons)
    if answ == "":
        answ = "Не найдено"
        keyboard = keyboards.keyboardadmin()
    await message.answer(answ, reply_markup=keyboard)
    await FMSAdmin.connectionpass.set()


@dp.message_handler(lambda message: message.text == "Добавить комментарий", state=FMSAdmin.connectionpass)
async def list(message: types.Message, state: FSMContext):
    await message.answer("Введите желаемый комментарий")
    await FMSAdmin.next()
    await FMSAdmin.next()


@dp.message_handler(state=FMSAdmin.add_comment)
async def list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    BotDB.add_information(data.get("finded"), "reviewed", message.text)
    await message.answer("Комментарий успешно добавлен", reply_markup=keyboards.keyboardadmin())
    await FMSAdmin.connectionpass.set()


@dp.message_handler(lambda message: message.text == "Режим пользователя", state=FMSAdmin.connectionpass)
async def list(message: types.Message, state: FSMContext):
    await message.answer("Вы в режиме Пользователя")
    await state.finish()
    await start(message)


# стартовая страница
@dp.message_handler(commands="start")
async def start(message: types.Message):
    me = await bot.get_me()

    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id,
                                   (
                                       f"Здравствуйте, {message.from_user.first_name} 👋 Я {me.first_name} помогу"
                                       f"ответить на Ваш вопрос. Что Вы хотели бы узнать?"),
                                   reply_markup=keyboards.keyboarduser())


@dp.message_handler(lambda message: message.text == "Проверить статус заявки")
async def without_puree(message: types.Message):
    await message.answer(str(BotDB.get_status(message.from_user.id))[3:-4])


@dp.message_handler(lambda message: message.text == "FAQ")
async def without_puree(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, позвольте быстро ввести Вас в курс дела и рассказать о том, что именно я умею 🐻\n\nЯ - КроноцкийБот, прямо в данном чате Вы можете заполнить заявку волонтера, задать вопрос по поводу волонтерской деятельности в формате текста или голосового сообщения, на который я очень-очень постараюсь дать верный ответ")


@dp.message_handler(lambda message: message.text == "О заповеднике")
async def without_puree(message: types.Message):
    await message.answer("""Мы сохраняем заповедные территории Камчатки и пробуждаем любовь к природе 🌱❤️

Наша организация – высокопрофессиональное экспертное сообщество с большим опытом природоохранной работы, который выходит за рамки вверенных нам природоохранных территорий. Мы стремимся содействовать решению региональных и российских проблем, связанных с экологией, природопользованием, сохранением редких и промысловых видов, подготовкой профессиональных кадров в сфере управления природными ресурсами и экологическим воспитанием подрастающего поколения.

Подробнее обо всем вы можете узнать на сайте заповедника - www.kronoki.ru""")


# @dp.message_handler(state=None)
# async def without_puree(message: types.Message):
#     question = message.text
#     if question != "Заполнить заявку":
#         result = searching.theBotMind(question)
#         await message.answer(result)


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
    check = State()
    checkmain = State()


# Начало диалога
@dp.message_handler(lambda message: message.text == "Заполнить заявку", state=None)
async def cm_start(message: types.Message):
    await FSMAnket.full_name.set()
    await message.answer("Для заполнения анкеты напишите свое ФИО 👤", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=None)
async def without_puree(message: types.Message):
    question = message.text
    if question != "Заполнить заявку":
        result = searching.theBotMind(question)
        await message.answer(result)
        if result == """После получения подтверждения отбора Вашей кандидатуры, при постановке в график, учитываются Ваши пожелания по территориям ООПТ для осуществления добровольческой деятельности.
В случае если график групп на данную территорию переполнен, Вам будет предложена другая территория, при наличии свободных мест.
Ознакомиться с актуальным графиком набора волонтеров можно на сайте www.kronoki.ru, либо по ссылке https://kronoki.ru/ru/volunteerism/programs/
При положительном решении, Вы получаете от нас письмо с приложениями:
договор о добровольческой деятельности для ознакомления:
1. с техническим заданием
2. с согласием на обработку персональных данных
3. правилами нахождения на территории.""":
            await message.answer("Ниже прикреплён договор в волонтёрской деятельности:")
            await dp.bot.send_document(message.from_user.id,
                                       "BQACAgIAAxkBAAILT2Gsc_kWe6Gisvc4ZRswOCQniqOCAAJbEQACRWVpSaagd7quCfD8IgQ")


# @dp.message_handler(content_types=types.ContentType.DOCUMENT, state=None)
# async def send_order_finish(message: types.Message, state: FSMContext):
#     msg_document = message.document.file_id
#     print("auf")
#     # await dp.bot.send_document(775430746, msg_document)
#     print(msg_document)
#     await state.reset_state()

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
    await message.answer("Почему именно Вы должны стать волонтером? 🌟 \n\nРасскажите коротко о себе и своих качествах",
                         reply_markup=types.ReplyKeyboardRemove())


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
    # await FSMAnket.next()
    await state.finish()
    # await message.answer("Ваша анкета заполнена, хотите проверить свои основные данные? 👀",
    #                      reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Ваша анкета заполнена, и направлена модератору 👀",
                         reply_markup=types.ReplyKeyboardRemove())
    await start(message)


# # Добавка к анкете
# @dp.message_handler(state=FSMAnket.check)
# async def load_birthday(message: types.Message, state: FSMContext):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Да", "Нет"]
#     keyboard.add(*buttons)
#     await state.finish()
#     await message.answer("*ожидаю ответ*",reply_markup=keyboard)
#
#
# @dp.message_handler(state=FSMAnket.checkmain)
# async def load_birthday(message: types.Message, state: FSMContext):
#     if message.text == "Да":
#         await message.answer("Если вы где-то ошиблись, нажмите на 'Заполнить анкету'")
#     else:
#         pass
#     await state.finish()
#     await message.answer(
#         "Спасибо, Ваша заявка оправлена модератору и скоро будет обработана.\nСтатус заявки Вы можете узнать в главном меню",
#         reply_markup=types.ReplyKeyboardRemove())
#     keyboards.keyboarduser()

