import sqlite3
import datetime 

class SQLite_conn:

    def __init__(self, database):
        """ коннектимся к базе данных и добавляем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_add(self, user_id, date_reg = datetime.datetime.now()):
        """добавляем нового пользователя"""
        print (date_reg)

        with self.connection:
            return self.cursor.execute("INSERT INTO `user` (`user_id`, `date_reg`) VALUES(?,?)", (user_id, date_reg))

    def user_exists(self, user_id):
        """получаем всех пользователей"""
        with self.connection:
            return self.cursor.execute("Select * FROM `user`").fetchall()
    
    def close(self):
        """закрываем соединение с БД"""
        self.connection.close()
