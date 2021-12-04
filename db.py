import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        print(self.cursor.execute("SELECT * FROM 'users'").fetchall())

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
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()


    def add_information(self, user_id, columns, value):
        """Добавляем информацию о пользователе"""
        columns = [""]
        name_of_columns = ""
        self.cursor.execute("UPDATE `users` SET ? = ? WHERE id = ?",
            (name_of_columns, value, user_id,))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()