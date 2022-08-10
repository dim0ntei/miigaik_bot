from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Обычные кнопки
YES = KeyboardButton(text='Да!', )
actually = KeyboardButton(text='Определенно да')
no_doubt = KeyboardButton(text='Вне всяких сомнений')
search_by_option = KeyboardButton(text='Поиск по варианту')
custom_works = KeyboardButton(text='Работы на заказ')
extra = KeyboardButton(text='Дополнительно')

# Инлайн кнопки
yes = InlineKeyboardButton(text='Да', callback_data='yes')
no = InlineKeyboardButton(text='Нет', callback_data='no')
back = InlineKeyboardButton(text='Назад', callback_data='back')
cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
try_again_b = InlineKeyboardButton(text='Еще раз', callback_data='try_again')
back_to_menu = InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')
FGiIB = InlineKeyboardButton(text='ФГиИБ', callback_data='ФГиИБ')
GF = InlineKeyboardButton(text='ГФ', callback_data='ГФ')
KF = InlineKeyboardButton(text='КФ', callback_data='КФ')
FOP = InlineKeyboardButton(text='ФОП', callback_data='ФОП')
ARH = InlineKeyboardButton(text='АРХ', callback_data='ФРХ')
FUT = InlineKeyboardButton(text='ФУТ', callback_data='ФУТ')
year_20_21 = InlineKeyboardButton(text='2020-2021', callback_data='2020-2021')
year_21_22 = InlineKeyboardButton(text='2021-2022', callback_data='2021-2022')
autumn_sem = InlineKeyboardButton(text='Осенний семестр', callback_data='осенний семестр')
spring_sem = InlineKeyboardButton(text='Весенний семестр', callback_data='весенний семестр')
buy_ready = InlineKeyboardButton(text='Купить готовую работу', callback_data='buy_ready')
executors = InlineKeyboardButton(text='Список исполнителей', callback_data='executors')
registration = InlineKeyboardButton(text='Регистрация', callback_data='registration')
correct = InlineKeyboardButton(text='Внести исправление', callback_data='correct')
phone_book = InlineKeyboardButton(text='Телефонный справочник', callback_data='phone_book')


# Обычные клавиатуры
hello = ReplyKeyboardMarkup(resize_keyboard=True,
                            one_time_keyboard=True,
                            row_width=2).add(YES, actually).row(no_doubt)
main_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True,
                                row_width=2).add(search_by_option).row(custom_works, extra)

# Инлайн клавиатуры
back_butt = InlineKeyboardMarkup().add(back)
confirmation = InlineKeyboardMarkup().row(yes, no)
faculty = InlineKeyboardMarkup().row(FGiIB, GF).row(KF, FOP).row(ARH, FUT).add(back)
year = InlineKeyboardMarkup().row(year_20_21, year_21_22)
sem = InlineKeyboardMarkup().row(autumn_sem, spring_sem)
one_more = InlineKeyboardMarkup().add(try_again_b).add(back)
executors_menu = InlineKeyboardMarkup().add(executors).add(buy_ready).add(back)
additional_menu = InlineKeyboardMarkup().add(registration).add(correct).row(phone_book, back)
