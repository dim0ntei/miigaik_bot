from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
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


@dp.message_handler(Text(equals='Да!'))
@dp.message_handler(Text(equals='Определенно да'))
@dp.message_handler(Text(equals='Вне всяких сомнений'))
async def start_menu(message: types.Message):
    await message.answer('Основное меню',
                         reply_markup=tg_keyboards.main_menu)


class SearchByOption(StatesGroup):
    faculty = State
    year = State
    sem = State
    group = State
    var = State
    confirmation = State
    end = State
    error = State
    sen_error = State


available_faculty = ['ФГиИБ', 'ГФ', 'КФ', 'ФОП', 'АРХ', 'ФУТ']


@dp.message_handler(Text(equals='Поиск по варианту', ignore_case=True))
async def search_by_option(message: types.Message):
    await message.answer('[Об этой функции](https://telegra.ph/Funkciya-poisk-po-variantu-08-09)\n'
                         'Выбери свой факультет',
                         parse_mode="Markdown",
                         reply_markup=tg_keyboards.faculty)


@dp.message_handler()
async def unknown(message: types.Message):
    await message.answer('Я тебя не понимаю. Воспользуйся кнопками.')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
