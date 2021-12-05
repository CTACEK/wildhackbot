import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))

        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM users WHERE `user_id` = ? VALUES(user_id);""")
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?);", (user_id,))
        return self.conn.commit()

    def get_bd(self, ):
        return self.cursor.execute("SELECT * FROM users;").fetchall()

    def add_information(self, user_id, name_of_column, value):
        """Добавляем информацию о пользователе"""
        # columns = ["user_id", "full_name", "date_of_application", "mail", "birthday", "phone_number", "education",
        #           "territory", "arrival_date", "departure_date", "lang", "experience", "skills", "recommendations",
        #           "volunteer_book", "pitch", "video", "reviewed"]

        self.cursor.execute(
            "UPDATE users SET '{0}' = '{1}' WHERE user_id = '{2}';".format(name_of_column, value, user_id))

        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
