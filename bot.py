#!/home/dmitry/tgBot/venv/bin/python
import config
import logging

from aiogram import Bot, Dispatcher, executor, types

# yroven log
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# hendler na komandy /about
@dp.message_handler(commands="about")
async def cmd_test1(message: types.Message):
    await message.reply("""
    О боте, что я умею:
        - вести учет расходов
        - трекер дел
        - записи
    """)

#  echo
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)



# run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)