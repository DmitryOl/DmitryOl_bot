import sqlite3
import datetime 

class SQLite_conn:

    def __init__(self, database):
        """ коннектимся к базе данных и добавляем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_add(self, id_user, data_reg = datetime.datetime.now()):
        """добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `user` (`id_user`, `data_reg`) VALUES(?,?)", (id_user, data_reg))

    def user_exists(self):
        """получаем всех пользователей"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `user` ").fetchall()

    def user_find(self, id_user):
        """есть ли такой пользователь?"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `user` WHERE `id_user` = ?', (id_user,)).fetchall()
            return bool(len(result))
    
    def close(self):
        """закрываем соединение с БД"""
        self.connection.close()

