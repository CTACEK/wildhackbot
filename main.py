import telebot
import config
import random
# import sqlite3
from telebot import types
from database import *

bot = telebot.TeleBot(config.token)

# connect = sqlite3.connect('servicedata.db')
# cursor = connect.cursor()


# def create():
#     cursor.execute("""CREATE TABLE IF NOT EXISTS servicedata(
#             id_data integer PRIMARY KEY,
#             value_data INTEGER
#     )""")
#
#     connect.commit()
#
#
# def delete_db():
#     cursor.execute("DROP TABLE servicedata")
#     connect.commit()
#     # cursor.close()
#
#
# def search_db():
#     cursor.execute("SELECT * FROM users")
#     all_results = cursor.fetchall()
#     print(all_results[0][1])


# def add(database,id,value):
#     data = [id, value]
#     cursor.execute("INSERT INTO database VALUES(?,?);", data)
#     connect.commit()


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('main2.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("✨ Удивительное предсказание")
    item3 = types.KeyboardButton("О Создательнице ❤️")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, вы попали в мир предсказаний и волшебства".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['admin'])
def access(message):
    send = bot.send_message(message.chat.id, "Введите пароль админа:")
    bot.register_next_step_handler(send, check)


def check(message):
    if message.text == password:
        adminka(message)
    else:
        bot.send_message(message.chat.id, "Иди отсюда падла, ты не одмен")


def adminka(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    admin1 = types.KeyboardButton("Ввести новое предсказание")
    admin2 = types.KeyboardButton("Статистика")
    admin3 = types.KeyboardButton("На начало")
    admin4 = types.KeyboardButton("Новый пароль")
    keyboard.add(admin1, admin2, admin3, admin4)
    request = bot.send_message(message.chat.id, "Вы вошли в режим одмена", reply_markup=keyboard)
    sti = open('keksi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.register_next_step_handler(request, adminmenu)


def passrequest(message):
    request = bot.send_message(message.chat.id, "Уверен в смене пароля?")
    bot.register_next_step_handler(request, perehod)


def perehod(message):
    yes = ['Да', 'да', 'ага', 'Ага']
    no = ['Нет', 'нет', 'неа']
    if message.text in yes:
        changepass(message)
    elif message.text in no:
        bot.send_message(message.chat.id, "Ну и ладно")
        adminka(message)


def changepass(message):
    global password
    passwo = bot.send_message(message.chat.id, "Придумай новый пароль")
    bot.register_next_step_handler(passwo, change)


def change(message):
    global password
    if message.text != '':
        password = str(message.text)
        bot.send_message(message.chat.id, f"Пароль изменён на '{password}'")
        adminka(message)
    else:
        changepass(message)


def adminmenu(message):
    global preds_count, random_count
    if message.text == 'Ввести новое предсказание':
        preds = bot.send_message(message.chat.id, str(f'Введите предсказание (сначала номер :)'))
        bot.register_next_step_handler(preds, addpreds)
        # data = [id, value]
        # cursor.execute("INSERT INTO predicts VALUES(?,?);", data)
        # connect.commit()



    elif message.text == 'Новый пароль':
        passrequest(message)


    elif message.text == 'Статистика':
        bot.send_message(message.chat.id, str(
            f'Кнопку рандомное число нажало {random_count} раз\nСвоё предсказание узнало уже {preds_count} раз'))
        wait(message)


    elif message.text == 'На начало':
        welcome(message)

    else:
        bot.send_message(message.chat.id, f'Ты какой-то странный, иди лучше на старт')
        welcome(message)


def wait(message):
    waiting = bot.send_message(message.chat.id, str(f'Фто дальфе, кеп?'))
    bot.register_next_step_handler(waiting, adminmenu)


def addpreds(message):
    global preds
    temp = str(message.text)
    preds[str(len(preds.keys()) + 1)] = temp
    bot.send_message(message.chat.id, str(f'В банк предсказаний добавлено: {temp}'))
    wait(message)


@bot.message_handler(content_types=['text'])
def processingoperations(message):
    global preds_count, random_count
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
            random_count += 1
        elif message.text == '✨ Удивительное предсказание':
            bot.send_message(message.chat.id, str(preds[str(random.randint(1, len(preds)))]))
            preds_count += 1
        elif message.text == 'О Создательнице ❤️':
            bot.send_message(message.chat.id, str(
                'Приветули, Я - Дарья, или же Создательница этого волшебного бота, который предскажет Вам ваше будущее 🔮🤭\nЯ учусь в 11 классе и это так тяжело, что Я была вынуждена создать бота-милашку, который будет предсказывать Вам только лучшее будущее ❤'))
            sti = open('profile.jpg', 'rb')
            bot.send_sticker(message.chat.id, sti)
        elif message.text == 'Пароль' or message.text == 'пароль':
            bot.send_message(message.chat.id, f'Актуальный пароль от админки: "{password}"')
        elif message.text == 'Кекс':
            stisw = open('keksi.webp', 'rb')
            bot.send_sticker(message.chat.id, stisw)
        else:
            bot.send_message(message.chat.id, 'У меня нет такой функции 😢')


if __name__ == '__main__':
    bot.infinity_polling()
