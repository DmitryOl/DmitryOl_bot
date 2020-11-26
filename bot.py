import config
import logging

from aiogram import Bot, Dispatcher, executor, types

# yroven log
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

#  echo
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

# run long polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)