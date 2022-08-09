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
back = InlineKeyboardButton(text='Назад', callback_data='back')
cancel = InlineKeyboardButton(text='Отмена', callback_data='cancel')
FGiIB = InlineKeyboardButton(text='ФГиИБ', callback_data='FGiIB')
GF = InlineKeyboardButton(text='ГФ', callback_data='GF')
KF = InlineKeyboardButton(text='КФ', callback_data='KF')
FOP = InlineKeyboardButton(text='ФОП', callback_data='FOP')
ARH = InlineKeyboardButton(text='АРХ', callback_data='ARH')
FUT = InlineKeyboardButton(text='ФУТ', callback_data='FUT')
year_20_21 = InlineKeyboardButton(text='2020-2021', callback_data='year_20_21')
year_21_22 = InlineKeyboardButton(text='2021-2022', callback_data='year_21_22')


# Обычные клавиатуры
hello = InlineKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=True,
                             row_width=2).add(YES, actually).row(no_doubt)
main_menu = InlineKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2).add(search_by_option).row(custom_works).row(extra)

# Инлайн клавиатуры
faculty = InlineKeyboardMarkup().row(FGiIB, GF).row(KF, FOP).row(ARH, FUT).add(back)
year = InlineKeyboardMarkup().row(year_20_21, year_21_22)
