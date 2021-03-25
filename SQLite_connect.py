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



import re


db = SQLite_conn('database/db_tgBot.db')

user_id = "0010"
mess = "testovich test"

if (not db.user_find(user_id)):
    # если новый, добавляем в базу
    db.user_add(user_id)


strs = []
strs.append("300 еда обед на работе")
strs.append("1000.50 развлечения сходили с друзьями в кальян бар")
strs.append("Сделал зарядку 0:10")
strs.append("ммразминка")
strs.append("м Сделать такую штукку которой нет ни у кого")

'''
for ret in strs:

    rslt = ret.split(' ')
    print(rslt)
    if rslt[0] == 'м' or rslt[0] == 'М':
        mes = re.sub('^\w{1}\s+', '', ret)
        db.add_mess_mind(user_id, mes)
        print(re.sub('^\w{1}\s+', '', ret))
    elif re.search('^\d', rslt[0]):
        val = rslt[0]
        cat = rslt[1]
        note = ' '.join(rslt[2:])
        db.add_mess_wal(user_id, val, cat, note)
        print(f"{user_id}, {val}, {cat}, {note}")

    elif re.search('^\w+', rslt[0]):
        if re.search('\d+:\d\d', rslt[-1]):
            times = rslt[-1]
            note = ' '.join(rslt[:-1])
            db.add_mess_action(user_id, note, times)
            print(f"{note} + {times}") 
        else:
            note = ret
            db.add_mess_action(user_id, note)
            print(note)
     
'''
    # print(rslt)

# aa = re.sub('^\d+', '', c)

# print (c)
# print("Это: ", aa)

# db.add_mess(user_id, mess)
# db.update_user(user_id, mess)
all_user = db.user_exists('wallet') 
print(all_user)
