#!/home/dmitry/DmitryOl_bot/venv/bin/python
import config
import logging

import platform
import subprocess
from aiogram import Bot, Dispatcher, executor, types

# yroven log
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# hendler na komandy /about
@dp.message_handler(commands="about")
async def about(message: types.Message):
    await message.reply("""
    О боте, что я умею:
        - вести учет расходов
        - трекер дел
        - записи
    """)

# hendler na komandy /cmd
@dp.message_handler(commands="cmd")
async def cmd(message: types.Message):
    if message.text == "/cmd":
        # command = 'git status '
            per = check_cmd()
            await message.answer(per)
    else:
        await message.answer(message.text)


#  echo
@dp.message_handler()
async def echo(message: types.Message):
    if message.text[:3] == 'cmd' and config.M_C_ID == str(message.chat.id) :
        per = check_cmd(message.text[3:])
        await message.answer(f"{message.text[3:]} :\n {per}")
    else:
        await message.answer(f"нет прав на запуск команды: {message.text}")

    await message.answer("я все равно запускаюсь!!!!")



#вынести проверку в отдельный файл
def check_cmd(cmd=""):    
    if cmd != '':
        return subprocess.check_output(cmd, shell = True).decode('utf-8')
    else:
        return f"запуск на {platform.system()} "



# run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)