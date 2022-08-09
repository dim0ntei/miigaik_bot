from vkbottle import Keyboard, EMPTY_KEYBOARD, Text

empty_keyboard = EMPTY_KEYBOARD

hello = (
    Keyboard(one_time=False, inline=False)
    .add(Text('Да!'))
    .add(Text('Определенно да'))
    .row()
    .add(Text('Вне всяких сомнений'))
    .get_json()
)

main_menu = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Поиск по варианту"))
    .row()
    .add(Text("Работы на заказ"))
    .row()
    .add(Text("Дополнительно"))
    .get_json()
)

faculty = (
    Keyboard(one_time=True, inline=False)
    .add(Text("ФГиИБ"))
    .add(Text("ГФ"))
    .row()
    .add(Text("КФ"))
    .add(Text("ФОП"))
    .row()
    .add(Text("АРХ"))
    .add(Text("ФУТ"))
    .get_json()
)

faculty_who_for = (
    Keyboard(one_time=True, inline=False)
    .add(Text("ФГиИБ"))
    .add(Text("ГФ"))
    .row()
    .add(Text("КФ"))
    .add(Text("ФОП"))
    .row()
    .add(Text("АРХ"))
    .add(Text("ФУТ"))
    .row()
    .add(Text("Назад"))
    .get_json()
)

year = (
    Keyboard(one_time=True, inline=False)
    .add(Text("2020-2021"))
    .add(Text("2021-2022"))
    .get_json()
)

sem = (
    Keyboard(one_time=True, inline=False)
    .add(Text("осенний семестр"))
    .add(Text("весенний семестр"))
    .get_json()
)

confirmation = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Да"))
    .add(Text("Нет"))
    .get_json()
)

works_menu = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Список исполнителей'))
    .row()
    .add(Text('Купить готовую работу'))
    .row()
    .add(Text('Гарант'))
    .add(Text('Назад'))
    .get_json()
)

course = (
    Keyboard(one_time=True, inline=False)
    .add(Text('1'))
    .add(Text('2'))
    .row()
    .add(Text('3'))
    .add(Text('4'))
    .add(Text('5'))
    .get_json()
)

additional_menu = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Зарегистрироваться'))
    .row()
    .add(Text('Внести исправление'))
    .row()
    .add(Text('Телефонный справочник'))
    .row()
    .add(Text('Назад'))
    .get_json()
)

phone_book = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Деканаты'))
    .row()
    .add(Text('Кафедры'))
    .row()
    .add(Text('Иное'))
    .add(Text('Назад'))
    .get_json()
)

cancel = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Отмена'))
    .get_json()
)

registration = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Стать исполнителем'))
    .row()
    .add(Text('Начать продавать'))
    .row()
    .add(Text('Назад'))
    .get_json()
)

become_executor = (
    Keyboard(one_time=True, inline=False)
    .add(Text(''))
)
