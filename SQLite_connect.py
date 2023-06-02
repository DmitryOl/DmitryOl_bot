import sqlite3
import datetime 
tablelist = {
    "user": "id_user INTEGER  PRIMARY KEY NOT NULL, name STRING, data_reg TIME, \
             last_mes_data DATETIME, last_mes_id INT, last_mes TEXT",
    "wallet": "wallet_id INTEGER PRIMARY KEY AUTOINCREMENT, wallet_cat TEXT REFERENCES categories (category),\
              wallet_id_user INT REFERENCES user (id_user), wallet_value DOUBLE, \
              wallet_note TEXT, wallet_datatime DATETIME",
    "mind_notes": "mind_id INTEGER PRIMARY KEY AUTOINCREMENT, mind_id_user INTEGER REFERENCES \
                    user (id_user) ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL, mind_datatime DATETIME, \
                    mind_note TEXT NOT NULL",
    "action_notes": "action_id INTEGER PRIMARY KEY AUTOINCREMENT, action_id_user INTEGER REFERENCES user (id_user), \
                       action_datatime DATETIME, action_note TEXT NOT NULL, action_time DATETIME",
    "download": "user_id INT, type TEXT, link TEXT, title TEXT, date DATETIME",
}

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
 
    def check_table(self):
        with self.connection:
            for table in tablelist:
                if not self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchall():
                    self.cursor.execute(f"CREATE TABLE {table} ({tablelist[table]})")

    def close(self):
        """закрываем соединение с БД"""
        self.connection.close()

