from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3


# функция вывода заглушки
def theGetPatch():
    return 'Извините, я всего лишь бот, у меня лапки🐻 \nВ случае, если Вы не можете определиться с вопросом или не ' \
           'знаете, как правильно его задать, можете воспользоваться списком часто задаваемых вопросов и выбрать ' \
           'один из них 📝'


def theTextFilter(text):  # приведение текста к единому формату
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    text = ''.join(text)
    return text


def theGetAnswerByTarget(question):  # получение ответа
    texts = []  # реплики
    module = []  # их ключи

    conn = sqlite3.connect("E:/Яна/Загрузки/Telegram Desktop/questions.sqlite3")
    cur = conn.cursor()
    db = cur.execute("SELECT * from data_config;").fetchall()

    data_config_with_db = {}
    for row in db:
        data_config_with_db[row[0]] = {'examples': row[1].split(';'), 'responses': [row[2]]}

    # заполнение списков "реплики" и "ключи"
    for intent, intent_data in data_config_with_db.items():
        for example in intent_data['examples']:
            texts.append(example)
            module.append(intent)

    # векторизация
    vectorizer = CountVectorizer()
    vector = vectorizer.fit_transform(texts)

    # выбор
    clf = LogisticRegression().fit(vector, module)
    probas = clf.predict_proba(vectorizer.transform([question]))[0]

    # проверка на ошибку и вывод ответа
    if max(probas) < 0.17:
        return None
    else:
        preResult = clf.predict(vectorizer.transform([question]))[-1]
        return data_config_with_db[preResult]['responses'][-1]


# основная функция бота
def theBotMind(question):
    # проверка на ошибки
    target = theTextFilter(question)

    # результат
    if target:
        answer = theGetAnswerByTarget(target)
        if answer:
            return answer

    # заглушка
    patch = theGetPatch()
    return patch

# # запуск кода
# question = None
#
# while question not in ['exit', 'выход']:
#     question = input()
#     result = theBotMind(question)
#     print(result)
