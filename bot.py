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
        run_platform = platform.system()
        if run_platform == "Windows":
            command = "git status"
        elif run_platform == "Linux":
            # command = "cd /home/dmitry/DmitryOl_bot/ && git status && "
            command = "echo 'проверка запуска баш скрипта' "
        else:
            await message.answer("Другая система, не Windows и не Linux")
        per = subprocess.check_output(command, shell = True)
        await message.answer(per.decode('utf-8'))

    else:
        await message.answer(message.text)


#  echo
@dp.message_handler()
async def echo(message: types.Message):
    if message.text[:3] == 'cmd' and config.M_C_ID == str(message.chat.id) :
        command = message.text[3:]
        per = subprocess.check_output(command, shell = True)
        await message.answer(f"{message.text[3:]} :\n {per.decode('utf-8')}")

    else:
        await message.answer(message.text)



# run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)