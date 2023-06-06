#!/home/dmitry/DmitryOl_bot/venv/bin/python
import config
import logging
#from aiogram import Bot, Dispatcher, executor, types
from aiogram import *
from SQLite_connect import SQLite_conn

import platform
import subprocess
import re

from pytube import YouTube
import os
from time import sleep
# yroven log
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

#подключаемся к БД
if platform.system() == "Windows":
    db = SQLite_conn('db_tgBot.db')
elif platform.system() == "Linux":
    db = SQLite_conn('/home/dmitry/DmitryOl_bot/db_tgBot.db')
db.check_table()

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
    if message.text[:3] == 'cmd' and config.M_C_ID == str(message.chat.id) :
        per = check_cmd(message.text[3:])
        await message.answer(f"{message.text[3:]} :\n {per}")
    elif message.text[:3] == 'cmd' and config.M_C_ID != str(message.chat.id) :
        await message.answer(f"нет прав на запуск команды: {message.text[3:]}")
    elif message.text[:2] in ['yt', 'Yt'] and config.M_C_ID == str(message.chat.id) :
        chat_id = message.chat.id
        url = message.text[3:]
        yt = YouTube(url)
        if message.text.startswith == 'https://www.youtube.com/' or 'https://youtu.be/':
            await bot.send_message(chat_id, f"*Начинаю загрузку видео* : *{yt.title}*\n"
            f"*С канала *: [{yt.author}]({yt.channel_url})")
            await download_yt_video(yt, message, bot)
    elif message.text[:2] in ['ym', 'Ym'] and config.M_C_ID == str(message.chat.id):
        chat_id = message.chat.id
        url = message.text[2:]
        yt = YouTube(url)
        if message.text.startswith == 'https://www.youtube.com/' or 'https://youtu.be/':
            await download_yt_music(url, message, bot)
    else:
        add_mes(message.chat.id, message.text)
        await message.answer(f"ваше сообщение: {message.text}")


async def download_yt_video(yt, message, bot):
    stream = yt.streams.filter(progressive=True, file_extension="mp4", res="360p")
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}')
    with open(f"{message.chat.id}/{message.chat.id}", 'rb') as video:
        await bot.send_video(message.chat.id, video, caption=yt.title)
        os.remove(f"{message.chat.id}/{message.chat.id}")

async def download_yt_music(url, message, bot):
    yt = YouTube(url)
    name = f"{message.chat.id}.mp3"
    yt.streams.filter(only_audio=True).first().download(filename=name)
    with open(f"{name}", 'rb') as audio:
        await bot.send_audio(message.chat.id, audio, caption=f"{yt.title}")
        os.remove(f"{name}")


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