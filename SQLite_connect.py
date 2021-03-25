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

    def update_user(self, id_user, mes, data_reg = datetime.datetime.now()):
        with self.connection:
            return self.cursor.execute("UPDATE `user` SET `last_mes_data` = ?, `last_mes` = ? WHERE `id_user` = ?",( data_reg, mes, id_user))

    def user_exists(self , table = "user"):
        """получаем всех пользователей"""
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `{table}`").fetchall()

    def user_find(self, id_user):
        """есть ли такой пользователь?"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `user` WHERE `id_user` = ?', (id_user,)).fetchall()
            return bool(len(result))
    
    def add_mess(self, id_user, mes, data_reg = datetime.datetime.now()):
        """записываем в базу сообщение и id user"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `wallet` (`wallet_id_user`, `wallet_note`,`wallet_datatime`) VALUES(?,?,?)",(id_user, mes, data_reg))
            

    def add_mess_wal(self, id_user, val, cat, note, data_reg = datetime.datetime.now()):
        with self.connection:
            return self.cursor.execute("INSERT INTO `wallet` (`wallet_id_user`, `wallet_cat`, `wallet_value`, `wallet_note`, `wallet_datatime`) VALUES(?,?,?,?,?)",(id_user, val, cat, note, data_reg))
                
    def add_mess_mind(self, id_user, mes, data_reg = datetime.datetime.now()):
        with self.connection:
            return self.cursor.execute("INSERT INTO `mind_notes` (`mind_id_user`,`mind_note`,`mind_datatime`) VALUES(?,?,?)", (id_user, mes, data_reg))


    def add_mess_action(self, id_user, note, time = 0, data_reg = datetime.datetime.now()):
        with self.connection:
            return self.cursor.execute("INSERT INTO `action_notes` (`action_id_user`, `action_note`, `action_time`, `action_datatime`) VALUES(?,?,?,?)", (id_user, note, time, data_reg))
 
    
    def close(self):
        """закрываем соединение с БД"""
        self.connection.close()

