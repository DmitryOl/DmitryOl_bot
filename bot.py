#!/home/dmitry/DmitryOl_bot/venv/bin/python
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from SQLite_connect import SQLite_conn

import platform
import subprocess
import re


# yroven log
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

#подключаемся к БД
if platform.system() == "Windows":
    db = SQLite_conn('database/db_tgBot.db')
elif platform.system() == "Linux":
    db = SQLite_conn('/home/dmitry/DmitryOl_bot/database/db_tgBot.db')


# выводим всех пользоватлей
@dp.message_handler(commands="usr_db")
async def usr_db(message: types.Message):
    add_mes(message.chat.id, message.text)

    all_user = db.user_exists() 
    await message.answer(all_user)


# hendler na komandy /about
@dp.message_handler(commands="about")
async def about(message: types.Message):
    await message.reply("""
    О боте, что я хочу сделать:
        - вести учет расходов
        - трекер дел
        - записи
    Что я умею:
        - Определять на какой системе запущен /cmd
        - Отправлять серверу сообщения через "cmd "
    """)


# hendler na komandy /cmd
@dp.message_handler(commands="cmd")
async def cmd(message: types.Message):
    if message.text == "/cmd":
        per = check_cmd()
        await message.answer(per)
    elif config.M_C_ID == str(message.chat.id):
        await message.answer(f"run {message.text[4:]}")
        subprocess.run(message.text[4:], shell = True , stdin = None , input = None , stdout = None ,)

    else:
        await message.answer(message.text)


#  echo
# передать проверку в отдельный файл со своей логикой?
@dp.message_handler()
async def echo(message: types.Message):
    add_mes(message.chat.id, message.text)
    if message.text[:3] == 'cmd' and config.M_C_ID == str(message.chat.id) :
        per = check_cmd(message.text[3:])
        await message.answer(f"{message.text[3:]} :\n {per}")
    elif message.text[:3] == 'cmd' and config.M_C_ID != str(message.chat.id) :
        await message.answer(f"нет прав на запуск команды: {message.text[3:]}")
    else:
        await message.answer(f"ваше сообщение: {message.text}")



#вынести проверку в отдельный файл
def check_cmd(cmd=""):    
    if cmd != '':
        return subprocess.check_output(cmd, shell = True).decode('utf-8')
    else:
        return f"запуск на {platform.system()} "

def add_mes(user_id, user_mes):    
    if (not db.user_find(user_id)):
        # если новый, добавляем в базу
        db.user_add(user_id)

    # распределяем сообщения по подходящим таблицам
    rslt = user_mes.split(' ')
    if rslt[0] == 'м' or rslt[0] == 'М': # если первое слово "м" то в мысли
        mes = re.sub('^\w{1}\s+', '', user_mes)
        db.add_mess_mind(user_id, mes)

    elif re.search('^\d', rslt[0]):     # если первое слово цифры, то в кошель
        val = rslt[0]
        cat = rslt[1]
        note = ' '.join(rslt[2:])
        db.add_mess_wal(user_id, val, cat, note)

    elif re.search('^\w+', rslt[0]): # если первое слово буквы то в действия
        if re.search('\d+:\d\d', rslt[-1]):
            times = rslt[-1]
            note = ' '.join(rslt[:-1])
            db.add_mess_action(user_id, note, times)
        else:
            note = user_mes
            db.add_mess_action(user_id, note)


    
# run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)