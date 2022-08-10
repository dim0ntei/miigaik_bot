from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import tg_keyboards
import config
import logging
import sqlite3

conn = sqlite3.connect('list_of_students.db')
cur = conn.cursor()

API_TOKEN = config.tg_token
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'начать'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Это тестовый бот сообщества ВК "МИИГАИК - лучший вуз\n\n"'
                         'ММИГАиК - Лучший вуз?',
                         reply_markup=tg_keyboards.hello)


@dp.message_handler(Text(equals=['Да!', 'Определенно да', 'Вне всяких сомнений']))
async def start_menu(message: types.Message):
    await message.answer('Основное меню',
                         reply_markup=tg_keyboards.main_menu)


@dp.message_handler(commands=['exit'])
async def exit(message: types.Message):
    await message.answer('Возвращаемся в основное меню',
                         reply_markup=tg_keyboards.main_menu)


class SearchByOption(StatesGroup):
    faculty = State()
    year = State()
    sem = State()
    var = State()
    confirmation = State()
    end = State()
    error = State()
    send_error = State()


@dp.message_handler(Text(equals='Поиск по варианту', ignore_case=True))
async def search_faculty(message: types.Message):
    await SearchByOption.faculty.set()
    await message.answer('[Об этой функции](https://telegra.ph/Funkciya-poisk-po-variantu-08-09)',
                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выбери свой факультет',
                         reply_markup=tg_keyboards.faculty)


@dp.callback_query_handler(state=SearchByOption.faculty)
async def search_year(call: types.CallbackQuery, state: FSMContext):
    await SearchByOption.next()
    if call.data == 'back':
        await call.message.answer('Жмякни сюда\n\n'
                                  '/exit')
        await state.finish()
        await call.answer()
    else:
        call_data = call.data
        async with state.proxy() as data:
            data['faculty'] = call_data
        await call.message.edit_text('Выбери год')
        await call.message.edit_reply_markup(tg_keyboards.year)
        await call.answer()


@dp.callback_query_handler(state=SearchByOption.year)
async def search_sem(call: types.CallbackQuery, state: FSMContext):
    await SearchByOption.next()
    call_data = call.data
    async with state.proxy() as data:
        data['year'] = call_data
    await call.message.edit_text('Выбери семестр')
    await call.message.edit_reply_markup(tg_keyboards.sem)
    await call.answer()


@dp.callback_query_handler(state=SearchByOption.sem)
async def search_var(call: types.CallbackQuery, state: FSMContext):
    await SearchByOption.next()
    call_data = call.data
    async with state.proxy() as data:
        data['sem'] = call_data
    await call.message.edit_text('Введи искомый вариант')
    await call.answer()


@dp.message_handler(state=SearchByOption.var)
async def search_confirm(message: types.Message, state: FSMContext):
    await SearchByOption.next()
    message_text = message.text
    async with state.proxy() as data:
        data['var'] = message_text
        await message.answer(f"Ты выбрал факультет {data.get('faculty')} в {data.get('year')}, "
                             f"{data.get('sem')}\n\nВсе правильно?",
                             reply_markup=tg_keyboards.confirmation)


@dp.callback_query_handler(state=SearchByOption.confirmation)
async def result(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        try:
            async with state.proxy() as data:
                if data.get('faculty') == 'ФГиИБ':
                    faculty = 'fakultet_Geoinformatiki_i_informatsionnoj_bezopasnosti'
                elif data.get('faculty') == 'ГФ':
                    faculty = 'Geodezicheskij_fakultet'
                elif data.get('faculty') == 'КФ':
                    faculty = 'Kartograficheskij_fakultet'
                elif data.get('faculty') == 'ФОП':
                    faculty = 'fakultet_Opticheskogo_priborostroenija'
                elif data.get('faculty') == 'АРХ':
                    faculty = 'fakultet_Arhitektury_i_gastrointestinal'
                elif data.get('faculty') == 'ФУТ':
                    faculty = 'fakultet_Upravlenija_territorijami'

                if data.get('year') == '2020-2021':
                    if data.get('sem') == 'осенний семестр':
                        sem = 1
                    elif data.get('sem') == 'весенний семестр':
                        sem = 2
                elif data.get('year') == '2021-2022':
                    if data.get('sem') == 'осенний семестр':
                        sem = 3
                    elif data.get('sem') == 'весенний семестр':
                        sem = 4

                var = data.get('var')

                query_text = f"""SELECT group_name, first_name, last_name FROM {faculty} WHERE sem='{sem}' AND person_number='{var}' ORDER BY group_name"""
                answer = cur.execute(query_text).fetchall()
                final_answer = 'Студенты, подходящие под твой запрос:\n'

                if not answer:
                    final_answer = 'Никого не найдено. Скорее всего, вы задали некорректные условия (Например, ' \
                                   'введенный порядковый номер превышает количество человек в группе)'
                    await state.finish()

                for item in answer:
                    element = f"{item[0]} - {item[1]} {item[2]}\n"
                    final_answer += f"{element}"

                await call.message.edit_text(text=f"{final_answer}",
                                             reply_markup=tg_keyboards.one_more)
                await call.answer()
                await SearchByOption.end.set()

        except UnboundLocalError:
            await call.message.edit_text('Ошибка. Возможно, вы задали некорректные условия поиска. '
                                         'Попробуйте еще раз', reply_markup=tg_keyboards.one_more)
            await exit_or_no
            await call.answer()

    if call.data == 'no':
        await call.message.edit_text('Начни заново:)',
                                     reply_markup=tg_keyboards.faculty)
        await SearchByOption.faculty.set()
        await call.answer()


@dp.callback_query_handler(state=SearchByOption.end)
async def exit_or_no(call: types.CallbackQuery, state: FSMContext):
    await SearchByOption.error.set()
    if call.data == 'try_again':
        await call.message.edit_text("Выбери факультет")
        await call.message.edit_reply_markup(tg_keyboards.faculty)
        await SearchByOption.faculty.set()
        await call.answer()
    elif call.data == 'back':
        await call.message.answer('Жмякни сюда:\n\n'
                                  '/exit')
        await state.finish()
        await call.answer()


@dp.message_handler()
async def unknown(message: types.Message):
    await message.answer('Я тебя не понимаю. Воспользуйся кнопками.',
                         reply_markup=tg_keyboards.main_menu)


conn.commit()
if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
