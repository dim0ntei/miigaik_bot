from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import tg_keyboards
import config
import logging

API_TOKEN = config.tg_token
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'начать', 'help', 'помощь'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Это тестовый бот сообщества ВК "МИИГАИК - лучший вуз"')
    await message.answer('ММИГАиК - Лучший вуз?',
                         reply_markup=tg_keyboards.hello)


@dp.message_handler()
async def unknown(message: types.Message):
    await message.answer('Я тебя не понимаю. Воспользуйся кнопками.')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
