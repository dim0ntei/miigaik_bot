from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Кнопки
YES = KeyboardButton('Да!',)
actually = KeyboardButton('Определенно да')
no_doubt = KeyboardButton('Вне всяких сомнений')
# Клавиатуры
hello = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(YES, actually, no_doubt)
