import vkbottle
from vkbottle import Keyboard, EMPTY_KEYBOARD, Text, CtxStorage
from tokens import token
from vkbottle.bot import Bot, Message
import os.path
import sqlite3

REAL_PATH = os.path.relpath(__file__)[:os.path.relpath(__file__).rfind("/") + 1]

bot = Bot(token)
ctx = CtxStorage()

conn = sqlite3.connect('list_of_students.db')
cur = conn.cursor()

KEYBOARD_HELLO = (
    Keyboard(one_time=False, inline=False)
        .add(Text('Да!'))
        .add(Text('Определенно да'))
        .row()
        .add(Text('Вне всяких сомнений'))
        .get_json()
)

KEYBOARD_MAIN_MENU = (
    Keyboard(one_time=True, inline=False)
        .add(Text("Поиск по варианту"))
        .row()
        .add(Text("Работы на заказ"))
        .row()
        .add(Text("Дополнительно"))
        .get_json()
)

KEYBOARD_FACULTY = (
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

KEYBOARD_FACULTY_WHO_FOR = (
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

KEYBOARD_YEAR = (
    Keyboard(one_time=True, inline=False)
        .add(Text("2020-2021"))
        .add(Text("2021-2022"))
        .get_json()
)

KEYBOARD_SEM = (
    Keyboard(one_time=True, inline=False)
        .add(Text("осенний семестр"))
        .add(Text("весенний семестр"))
        .get_json()
)

KEYBOARD_CONFIRMATION = (
    Keyboard(one_time=True, inline=False)
        .add(Text("Да"))
        .add(Text("Нет"))
        .get_json()
)

KEYBOARD_WORKS_MENU = (
    Keyboard(one_time=True, inline=False)
        .add(Text('Список исполнителей'))
        .row()
        .add(Text('Купить готовую работу'))
        .row()
        .add(Text('Гарант'))
        .add(Text('Назад'))
        .get_json()
)

KEYBOARD_COURSE = (
    Keyboard(one_time=True, inline=False)
        .add(Text('1'))
        .add(Text('2'))
        .row()
        .add(Text('3'))
        .add(Text('4'))
        .add(Text('5'))
        .get_json()
)

KEYBOARD_ADDITIONAL_MENU = (
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

KEYBOARD_PHONE_BOOK = (
    Keyboard(one_time=True, inline=False)
        .add(Text('Деканаты'))
        .row()
        .add(Text('Кафедры'))
        .row()
        .add(Text('Иное'))
        .add(Text('Назад'))
        .get_json()
)

KEYBOARD_CANCEL = (
    Keyboard(one_time=True, inline=False)
        .add(Text('Отмена'))
        .get_json()
)

KEYBOARD_REGISTRATION = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Стать исполнителем'))
    .row()
    .add(Text('Начать продавать'))
    .row()
    .add(Text('Назад'))
    .get_json()
)

KEYBOARD_BECOME_EXECUTOR = (
    Keyboard(one_time=True, inline=False)
    .add(Text(''))
)


@bot.on.private_message(text='Начать')
async def hello(message: Message):
    await message.answer("МИИГАиК - лучший ВУЗ?", keyboard=KEYBOARD_HELLO)


@bot.on.private_message(text='Да!')
@bot.on.private_message(text='Определенно да')
@bot.on.private_message(text='Вне всяких сомнений')
@bot.on.private_message(text='Меню')
async def menu(message: Message):
    await message.answer("Функция из рекламы - поиск по варианту.")
    await message.answer("Основное меню:", keyboard=KEYBOARD_MAIN_MENU)


class WhoForStates(vkbottle.BaseStateGroup):
    who_for_faculty = 0
    who_for_year = 1
    who_for_sem = 2
    who_for_group = 3
    your_var = 4
    confirmation_who_for = 5
    who_for_end = 6
    who_for_error = 7
    who_for_error_send = 8


@bot.on.private_message(text='Поиск по варианту')
async def who_for_info(message: Message):
    await bot.state_dispenser.set(message.peer_id, WhoForStates.who_for_faculty)
    await message.answer("Об этой функции:\n\nvk.com/@miigaik_the_best-funkciya-poisk-po-variantu")
    await message.answer("Для начала, выбери факультет:", keyboard=KEYBOARD_FACULTY_WHO_FOR)


@bot.on.private_message(text='Назад', state=WhoForStates.who_for_faculty)
async def back_to_menu(message: Message):
    await message.answer("Возвращаемся в основное меню...", keyboard=KEYBOARD_MAIN_MENU)
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.private_message(state=WhoForStates.who_for_faculty)
async def who_for_year(message: Message):
    ctx.set('who_for_faculty', message.text)
    await bot.state_dispenser.set(message.peer_id, WhoForStates.who_for_year)
    await message.answer("В каком учебном году?", keyboard=KEYBOARD_YEAR)


@bot.on.private_message(state=WhoForStates.who_for_year)
async def who_for_sem(message: Message):
    ctx.set('year', message.text)
    await bot.state_dispenser.set(message.peer_id, WhoForStates.who_for_sem)
    await message.answer("В каком семестре?", keyboard=KEYBOARD_SEM)


@bot.on.private_message(state=WhoForStates.who_for_sem)
async def your_var(message: Message):
    ctx.set('sem', message.text)
    await bot.state_dispenser.set(message.peer_id, WhoForStates.your_var)
    await message.answer("Какой порядковый номер в списке группы? Введи цифрами:", keyboard=EMPTY_KEYBOARD)
    ctx.set('temp', message.text)


@bot.on.private_message(state=WhoForStates.your_var)
async def who_for_confirmation(message: Message):
    ctx.set('your_var', message.text)
    await bot.state_dispenser.set(message.peer_id, WhoForStates.confirmation_who_for)
    await message.answer(f"Ты выбрал факультет {ctx.get('who_for_faculty')} за {ctx.get('year')} учебный год, "
                         f"{ctx.get('sem')}, вариант {ctx.get('your_var')}. Все правильно?",
                         keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=WhoForStates.confirmation_who_for)
async def result(message: Message):
    ctx.set('who_for_confirmation', message.text)
    if ctx.get('who_for_confirmation') == 'Да':
        try:
            if ctx.get('who_for_faculty') == 'ФГиИБ':
                faculty = 'fakultet_Geoinformatiki_i_informatsionnoj_bezopasnosti'
            elif ctx.get('who_for_faculty') == 'ГФ':
                faculty = 'Geodezicheskij_fakultet'
            elif ctx.get('who_for_faculty') == 'КФ':
                faculty = 'Kartograficheskij_fakultet'
            elif ctx.get('who_for_faculty') == 'ФОП':
                faculty = 'fakultet_Opticheskogo_priborostroenija'
            elif ctx.get('who_for_faculty') == 'АРХ':
                faculty = 'fakultet_Arhitektury_i_gradostroitelstva'
            elif ctx.get('who_for_faculty') == 'ФУТ':
                faculty = 'fakultet_Upravlenija_territorijami'

            if ctx.get('year') == '2020-2021':
                if ctx.get('sem') == 'осенний семестр':
                    sem = 1
                elif ctx.get('sem') == 'весенний семестр':
                    sem = 2
            elif ctx.get('year') == '2021-2022':
                if ctx.get('sem') == 'осенний семестр':
                    sem = 3
                elif ctx.get('sem') == 'весенний семестр':
                    sem = 4

            var = ctx.get('your_var')

            query_text = f"""SELECT group_name, first_name, last_name FROM {faculty} WHERE sem='{sem}' AND person_number='{var}' ORDER BY group_name"""
            answer = cur.execute(query_text).fetchall()
            final_answer = 'Студенты, подходящие под твой запрос:\n'
            if not answer:
                final_answer = 'Никого не найдено. Скорее всего, вы задали некорректные условия (Например, ' \
                               'введенный порядковый номер превышает количество человек в группе)'

            for item in answer:
                element = f"{item[0]} - {item[1]} {item[2]}\n"
                final_answer += f"{element}"

            await message.answer(f'{final_answer}')
            await message.answer("Поддержать разработчика - 4274320109029440 (Сбер)")
            await message.answer("Возвращаемся в меню...", keyboard=KEYBOARD_MAIN_MENU)
            await bot.state_dispenser.delete(message.peer_id)

        except UnboundLocalError:
            await bot.state_dispenser.set(message.peer_id, WhoForStates.who_for_error)
            await message.answer("Ошибка. Возможно, вы задали некорректные условия поиска. "
                                 "Отправить отчет разработчику?", keyboard=KEYBOARD_CONFIRMATION)
    elif ctx.get('who_for_confirmation') == 'Нет':
        await message.answer("Начни заново:)", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)


@bot.on.private_message(state=WhoForStates.who_for_error)
async def who_for_error(message: Message):
    ctx.set('who_for_error_confirmation', message.text)
    if ctx.get('who_for_error_confirmation') == 'Да':
        user = await bot.api.users.get(message.from_id)
        await bot.api.messages.send(peer_id=375010066, message=f"Сообщение об ошибке в поиске по варианту от "
                                                               f"{user[0].first_name} {user[0].last_name}. "
                                                               f"Заданы следующие параметры отбора:\n\n"
                                                               f"Факультет {ctx.get('who_for_faculty')} за "
                                                               f"{ctx.get('year')} учебный год, {ctx.get('sem')}, "
                                                               f"вариант {ctx.get('your_var')}.\n\n"
                                                               f"#ошибка", random_id=0)
        await message.answer("Отчет отправлен администратору. Возвращаемся в меню...", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
    elif ctx.get('who_for_error_confirmation') == 'Нет':
        await message.answer("Возвращаемся в меню...", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
    elif ctx.get('who_for_error') != 'Да' or ctx.get('who_for_error') != 'Нет':
        await bot.state_dispenser.get(WhoForStates.who_for_error)
    await message.answer('Выберите «да» или «нет»', keyboard=KEYBOARD_CONFIRMATION)


class WorksMenuStates(vkbottle.BaseStateGroup):
    works_menu = 0


@bot.on.private_message(text='Работы на заказ')
async def executors_menu(message: Message):
    await bot.state_dispenser.set(message.peer_id, WorksMenuStates.works_menu)
    await message.answer("Почитать про работы на заказ можно здесь:\n\n"
                         "https://vk.com/@miigaik_the_best-razdel-raboty-na-zakaz",
                         keyboard=KEYBOARD_WORKS_MENU)


@bot.on.private_message(state=WorksMenuStates.works_menu, text="Назад")
async def back_to_menu(message: Message):
    await message.answer('Возвращаемся в основное меню...', keyboard=KEYBOARD_MAIN_MENU)
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.private_message(state=WorksMenuStates.works_menu, text='Список исполнителей')
async def executors_list(message: Message):
    await message.answer('В связи с тем, что исполнителей пока что мало, они выводятся одним списком. '
                         'В будущем будет фильтрация по факультету.', keyboard=KEYBOARD_WORKS_MENU)
    query_text = f"""SELECT name, faculty, about, link FROM executors"""
    exec_list = cur.execute(query_text).fetchall()
    final_exec_list = 'На данный момент зарегистрированы:\n\n'
    for executor in exec_list:
        element = f"Имя: {executor[0]}\n" \
                  f"Факультет: {executor[1]}\n" \
                  f"О себе: {executor[2]}\n" \
                  f"Ссылка на страницу: {executor[3]}\n\n"
        final_exec_list += f"{element}"
    if not exec_list:
        final_exec_list = 'Исполнителей пока что нет('
    await message.answer(f"{final_exec_list}", keyboard=KEYBOARD_WORKS_MENU)
    await message.answer('Подать заявку для включения в список можно в разделе «Дополнительно» -> «Зарегистрироваться».'
                         ' Это бесплатно!',
                         keyboard=KEYBOARD_WORKS_MENU)
    await bot.state_dispenser.set(message.peer_id, WorksMenuStates.works_menu)


@bot.on.private_message(state=WorksMenuStates.works_menu, text='Купить готовую работу')
async def ready_works_list(message: Message):
    await message.answer('Готовых продавать свои старые работы пока что нет. Станьте первым, это бесплатно! '
                         'Подать заявку для включения в список можно в разделе '
                         '«Дополнительно» -> «Зарегистрироваться».')
    query_text = f"""SELECT name, faculty, about, link, var FROM ready_works"""
    work_list = cur.execute(query_text).fetchall()
    final_work_list = 'на данный момент зарегистрированы:\n\n'
    for work in work_list:
        element = f"Имя: {work[0]}\n" \
                  f"Факультет: {work[1]}\n" \
                  f"Вариант: {work[4]}\n" \
                  f"О себе: {work[2]}\n" \
                  f"Ссылка на страницу: {work[3]}\n\n"
        final_work_list += f"{element}"
    if not work_list:
        final_work_list = 'Готовых продавать свои старые работы пока что нет :('
    await message.answer(f"{final_work_list}", keyboard=KEYBOARD_WORKS_MENU)


class GarantRequest(vkbottle.BaseStateGroup):
    start_garant_request = 0
    garant_request_customer = 1
    garant_request_executer = 2
    garant_request_task = 3
    garant_request_confirmation = 4
    send_garant_request = 5
    garant_request_end = 6


@bot.on.private_message(state=WorksMenuStates.works_menu, text='Гарант')
async def garant_request(message: Message):
    await bot.state_dispenser.set(message.peer_id, GarantRequest.start_garant_request)
    await message.answer("Настоятельно рекомендую ознакомиться с правилами работы сервиса «Гарант» здесь:\n\n"
                         "vk.com/@miigaik_the_best-garant-chto-i-zachem-pravila-ispolzovaniya-servisa"
                         "\n\nПродолжить оформление запроса?", keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=GarantRequest.start_garant_request)
async def garant_request_customer(message: Message):
    ctx.set('garant_request_confirmation', message.text)
    if ctx.get('garant_request_confirmation') == 'Да':
        await bot.state_dispenser.set(message.peer_id, GarantRequest.garant_request_customer)
        await message.answer("Отправьте ссылку на аккаунт ВК заказчика (Тот, кому помогают):",
                             keyboard=EMPTY_KEYBOARD)
    elif ctx.get('garant_request_confirmation') == 'Нет':
        await message.answer("Возвращаемся в меню...", keyboard=KEYBOARD_WORKS_MENU)
        await bot.state_dispenser.set(message.peer_id, WorksMenuStates.works_menu)


@bot.on.private_message(state=GarantRequest.garant_request_customer)
async def garant_request_executer(message: Message):
    ctx.set('garant_request_customer', message.text)
    await bot.state_dispenser.set(message.peer_id, GarantRequest.garant_request_executer)
    await message.answer("Отправьте ссылку на аккаунт ВК исполнителя:", keyboard=EMPTY_KEYBOARD)


@bot.on.private_message(state=GarantRequest.garant_request_executer)
async def garant_request_task(message: Message):
    ctx.set('garant_request_executer', message.text)
    await bot.state_dispenser.set(message.peer_id, GarantRequest.garant_request_task)
    await message.answer("Опишите поставленную перед исполнителем задачу. Если формулировка будет "
                         "неоднозначной, то в случае конфликта вопрос с большей вероятностью будет решен в пользу "
                         "стороны, представленной в невыгодном свете. Пример однозначной формулировки: \n\n"
                         "Решить 10 задач из РГР по математическому анализу, вариант 5. Решение расписано подробно, на "
                         "бумаге в клетку, разборчивым почерком. Готовую работу отправить заказчику в ВКонтакте. "
                         "Заказчик претендует не менее чем на 3 бесплатных исправления/поправки. Срок - до 10 мая. "
                         "Сумма заказа - 600 рублей")


@bot.on.private_message(state=GarantRequest.garant_request_task)
async def garant_request_confirmation(message: Message):
    ctx.set('garant_request_task', message.text)
    await bot.state_dispenser.set(message.peer_id, GarantRequest.send_garant_request)
    await message.answer(f"Заказчик - {ctx.get('garant_request_customer')}. Исполнитель - "
                         f"{ctx.get('garant_request_executer')}. Поставленная задача: \n\n"
                         f"{ctx.get('garant_request_task')} \n\n"
                         f"Отправляем заявку? Внимание: за спам полагается пожизненный бан.",
                         keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=GarantRequest.send_garant_request)
async def send_garant_request(message: Message):
    ctx.set('send_garant_request', message.text)
    if ctx.get('send_garant_request') == 'Да':
        user = await bot.api.users.get(message.from_id)
        await bot.api.messages.send(peer_id=375010066, message=f"Запрос на грантовую поддержку от "
                                                               f"{user[0].first_name} {user[0].last_name}. "
                                                               f"Заказчик - {ctx.get('garant_request_customer')}, "
                                                               f"исполнитель - {ctx.get('garant_request_executer')}. "
                                                               f"Поставленная задача: \n\n"
                                                               f"{ctx.get('garant_request_task')} \n\n"
                                                               f"#запроснагаранта", random_id=0)
        await message.answer("Запрос отправлен на модерацию. В случае одобрения вам придет сообщение в этот чат. "
                             "Возвращаемся в меню...", keyboard=KEYBOARD_WORKS_MENU)
        await bot.state_dispenser.get(WorksMenuStates.works_menu)

    elif ctx.get('send_garant_request') == 'Нет':
        await message.answer("Возвращаемся в меню...", keyboard=KEYBOARD_WORKS_MENU)
        await bot.state_dispenser.get(WorksMenuStates.works_menu)


class AdditionalMenuStates(vkbottle.BaseStateGroup):
    main = 0


@bot.on.private_message(text='Дополнительно')
async def additional_menu(message: Message):
    await bot.state_dispenser.set(message.peer_id, AdditionalMenuStates.main)
    await message.answer("Дополнительное меню", keyboard=KEYBOARD_ADDITIONAL_MENU)


@bot.on.private_message(text='Назад', state=AdditionalMenuStates.main)
async def additional_menu_back(message: Message):
    await message.answer("Возвращаемся в основное меню...", keyboard=KEYBOARD_MAIN_MENU)
    await bot.state_dispenser.delete(message.peer_id)


class RegistrationStates(vkbottle.BaseStateGroup):
    main = 0
    executor = 1
    executor_conf = 2
    executor_faculty = 3
    executor_about = 4
    executor_link = 5
    ready_work = 6
    ready_work_conf = 7
    ready_work_var = 8
    ready_work_faculty = 9
    ready_work_about = 10
    ready_work_link = 11
    ready_work_finish = 12


@bot.on.private_message(state=AdditionalMenuStates.main, text='Зарегистрироваться')
async def registration(message: Message):
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.main)
    await message.answer('Выберите, кем хотите стать. Исполнители выполняют работы на заказ, продавцы - продают свои '
                         'старые готовые работы.', keyboard=KEYBOARD_REGISTRATION)


@bot.on.private_message(state=RegistrationStates.main, text='Назад')
async def reg_back(message: Message):
    await message.answer('Возвращаемся...', keyboard=KEYBOARD_ADDITIONAL_MENU)
    await bot.state_dispenser.set(message.peer_id, AdditionalMenuStates.main)


@bot.on.private_message(state=RegistrationStates.main, text='Стать исполнителем')
async def executor_reg_conf(message: Message):
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.executor)
    await message.answer('Заполнить анкету?', keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=RegistrationStates.executor)
async def executor_reg_faculty(message: Message):
    ctx.set('executor_reg_conf', message.text)
    if ctx.get('executor_reg_conf') == 'Нет':
        await message.answer('Возвращаемся...', keyboard=KEYBOARD_REGISTRATION)
        await bot.state_dispenser.get(RegistrationStates.main)
    elif ctx.get('executor_reg_conf') == 'Да':
        await message.answer('С какого вы факультета?', keyboard=KEYBOARD_FACULTY)
        await bot.state_dispenser.set(message.peer_id, RegistrationStates.executor_faculty)
    elif ctx.get('executor_reg_conf') != 'Нет' or ctx.get('executor_reg_conf') != 'Да':
        await message.answer('Выберите «Да» или «Нет»', keyboard=KEYBOARD_CONFIRMATION)
        await bot.state_dispenser.get(RegistrationStates.executor)


@bot.on.private_message(state=RegistrationStates.executor_faculty)
async def executor_reg_about(message: Message):
    ctx.set('executor_reg_faculty', message.text)
    await message.answer('Напишите, за какие предметы вы готовы браться, какие типы работ предпочитаете (РГР, '
                         'курсовые, домашние работы и т.д. и т.п.)', keyboard=EMPTY_KEYBOARD)
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.executor_about)


@bot.on.private_message(state=RegistrationStates.executor_about)
async def executor_reg_link(message: Message):
    ctx.set('executor_reg_about', message.text)
    await message.answer('Отправьте ссылку на вашу страницу')
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.executor_link)


@bot.on.private_message(state=RegistrationStates.executor_link)
async def executor_send_conf(message: Message):
    ctx.set('executor_link', message.text)
    await message.answer('Отправить заявку? После одобрения вы будете отображаться в списке исполнителей в течении 3-х '
                         'месяцев.\n\nОбращаем внимание, что спам карается баном.', keyboard=KEYBOARD_CONFIRMATION)
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.executor_conf)


@bot.on.private_message(state=RegistrationStates.executor_conf)
async def executor_reg_end(message: Message):
    ctx.set('executor_reg_conf', message.text)
    if ctx.get('executor_reg_conf') == 'Да':
        user = await bot.api.users.get(message.from_id)
        await bot.api.messages.send(peer_id=375010066, message=f"Анкета исполнителя от {user[0].first_name} "
                                                               f"{user[0].last_name}:\n\n"
                                                               f"Факультет: {ctx.get('executor_reg_faculty')}\n"
                                                               f"О себе: {ctx.get('executor_reg_about')}\n"
                                                               f"Ссылка на страницу: {ctx.get('executor_link')}\n\n"
                                                               f"#анкетаисполнителя", random_id=0)
        await message.answer("Анкета отправлена. Возвращаемся...", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.get(RegistrationStates.main)
    elif ctx.get('executor_reg_conf') == 'Нет':
        await message.answer('Возвращаемся...', keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.get(WorksMenuStates.works_menu)
    elif ctx.get('executor_reg_conf') != 'Да' or ctx.get('executor_reg_conf') != 'Нет':
        await message.answer('Выберите «Да» или «Нет»', keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=RegistrationStates.main, text='Начать продавать')
async def executor_reg_conf(message: Message):
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work)
    await message.answer('Заполнить анкету?', keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=RegistrationStates.ready_work)
async def executor_reg_faculty(message: Message):
    ctx.set('ready_work_reg_conf', message.text)
    if ctx.get('ready_work_reg_conf') == 'Нет':
        await message.answer('Возвращаемся...', keyboard=KEYBOARD_REGISTRATION)
        await bot.state_dispenser.get(RegistrationStates.main)
    elif ctx.get('ready_work_reg_conf') == 'Да':
        await message.answer('С какого вы факультета?', keyboard=KEYBOARD_FACULTY)
        await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work_faculty)
    elif ctx.get('ready_work_reg_conf') != 'Нет' or ctx.get('executor_reg_conf') != 'Да':
        await message.answer('Выберите «Да» или «Нет»', keyboard=KEYBOARD_CONFIRMATION)
        await bot.state_dispenser.get(RegistrationStates.ready_work)


@bot.on.private_message(state=RegistrationStates.ready_work_faculty)
async def ready_work_reg_about(message: Message):
    ctx.set('ready_work_reg_faculty', message.text)
    await message.answer('Напишите, по каким предметам у вас есть готовые работы и их тип (РГР, '
                         'курсовые, домашние работы и т.д. и т.п.)', keyboard=EMPTY_KEYBOARD)
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work_var)


@bot.on.private_message(state=RegistrationStates.ready_work_var)
async def ready_work_var(message: Message):
    ctx.set('ready_work_reg_about', message.text)
    await message.answer('Какие у вас были варианты по каждому из этих предметов?')
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work_link)


@bot.on.private_message(state=RegistrationStates.ready_work_link)
async def ready_work_reg_link(message: Message):
    ctx.set('ready_work_reg_var', message.text)
    await message.answer('Отправьте ссылку на вашу страницу')
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work_finish)


@bot.on.private_message(state=RegistrationStates.ready_work_finish)
async def ready_work_send_conf(message: Message):
    ctx.set('ready_work_link', message.text)
    await message.answer('Отправить заявку? После одобрения вы будете отображаться в списке в течении 3-х '
                         'месяцев.\n\nОбращаем внимание, что спам карается баном.', keyboard=KEYBOARD_CONFIRMATION)
    await bot.state_dispenser.set(message.peer_id, RegistrationStates.ready_work_conf)


@bot.on.private_message(state=RegistrationStates.ready_work_conf)
async def ready_work_reg_end(message: Message):
    ctx.set('ready_work_reg_send', message.text)
    if ctx.get('ready_work_reg_send') == 'Да':
        user = await bot.api.users.get(message.from_id)
        await bot.api.messages.send(peer_id=375010066, message=f"Анкета готовых работ от {user[0].first_name} "
                                                               f"{user[0].last_name}:\n\n"
                                                               f"Факультет: {ctx.get('ready_work_reg_faculty')}\n"
                                                               f"О себе: {ctx.get('ready_work_reg_about')}\n"
                                                               f"Вариант: {ctx.get('ready_work_reg_var')}\n"
                                                               f"Ссылка на страницу: {ctx.get('ready_work_link')}\n\n"
                                                               f"#анкетаготовыхработ", random_id=0)
        await message.answer("Анкета отправлена. Возвращаемся...", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
    elif ctx.get('ready_work_reg_send') == 'Нет':
        await message.answer('Возвращаемся...', keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
        await bot.state_dispenser.get(WorksMenuStates.works_menu)
    elif ctx.get('ready_work_reg_send') != 'Да' or ctx.get('ready_work_reg_send') != 'Нет':
        await message.answer('Выберите «Да» или «Нет»', keyboard=KEYBOARD_CONFIRMATION)


class SuggestCorrection(vkbottle.BaseStateGroup):
    suggestion = 0
    confirm_suggest = 1
    send_suggest = 2


@bot.on.private_message(state=AdditionalMenuStates.main, text='Внести исправление')
async def suggest_correction(message: Message):
    await bot.state_dispenser.set(message.peer_id, SuggestCorrection.suggestion)
    await message.answer("Если вы считаете, что идете под неправильным порядковым номером или хотите внести изменение "
                         "телефонный справочник или просто что то предложить, то сформулируйте это одним сообщением "
                         "и отправьте в этот чат игнорируя кнопку отмены",
                         keyboard=KEYBOARD_CANCEL)


@bot.on.private_message(text='Отмена', state=SuggestCorrection.suggestion)
async def cancel(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    await bot.state_dispenser.set(message.peer_id, state=AdditionalMenuStates.main)
    await message.answer("Возвращаемся...", keyboard=KEYBOARD_ADDITIONAL_MENU)


@bot.on.private_message(state=SuggestCorrection.suggestion)
async def confirmation(message: Message):
    ctx.set('suggestion', message.text)
    await bot.state_dispenser.set(message.peer_id, SuggestCorrection.confirm_suggest)
    await message.answer("Отправить предложение?",
                         keyboard=KEYBOARD_CONFIRMATION)


@bot.on.private_message(state=SuggestCorrection.confirm_suggest)
async def send_confirmation(message: Message):
    ctx.set('confirm_suggestion', message.text)
    if ctx.get('confirm_suggestion') == 'Да':
        await bot.state_dispenser.set(message.peer_id, SuggestCorrection.send_suggest)
        user = await bot.api.users.get(message.from_id)
        await bot.api.messages.send(peer_id=375010066, message=f"Предложение об исправлении от {user[0].first_name} "
                                                               f"{user[0].last_name}:\n\n"
                                                               f"{ctx.get('suggestion')}\n\n"
                                                               f"#исправление", random_id=0)
        await message.answer("Предложение отправлено", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
    elif ctx.get('confirm_suggestion') == 'Нет':
        await message.answer("Возвращаемся в меню...", keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)


class PhoneBookStates(vkbottle.BaseStateGroup):
    phone_book_menu = 0


@bot.on.private_message(state=AdditionalMenuStates.main, text='Телефонный справочник')
async def phone_book_menu(message: Message):
    await bot.state_dispenser.set(message.peer_id, PhoneBookStates.phone_book_menu)
    await message.answer("Выберите раздел", keyboard=KEYBOARD_PHONE_BOOK)


@bot.on.private_message(state=PhoneBookStates.phone_book_menu)
async def phone_book(message: Message):
    ctx.set('phone_group', message.text)

    if ctx.get('phone_group') == 'Деканаты':
        await message.answer("Деканат геодезического факультета: \n"
                             "1) 8(499)404-12-20 доб. 2110\n"
                             "2) 8(925)934-49-80\n"
                             "email: geofak@miigaik.ru\n\n"
                             "Деканат картографического факультета:\n"
                             "8(499)404-12-20 доб. 2210\n"
                             "email: kartfak@miigaik.ru\n\n"
                             "Деканат факультета оптического приборостроения:\n"
                             "1) 8(499)261-37-41 доб. 2410\n"
                             "2) 8(925)934-49-37\n"
                             "email: fop@miigaik.ru\n\n"
                             "Деканат факультета геоинформатики и информационной безопасности:\n"
                             "8(499)404-12-20 доб. 2310\n"
                             "email: gis_faculty@miigaik.ru\n\n"
                             "Деканат факультета управления территориями:\n"
                             "1) 8(499)404-12-20 доб. 2510\n"
                             "2) 8(925)934-50-12\n"
                             "email: feut@feut.ru\n\n"
                             "Деканат факультета архитектуры и градостроительства:\n"
                             "1) 8(499)404-12-20 доб. 2610\n"
                             "2) 8(925)934-50-62\n"
                             "email: guf@miigaik.ru")
        await message.answer("Если вы точно уверены, что какой-либо из контактов неверен, используйте функцию "
                             "предложить исправление.", keyboard=KEYBOARD_PHONE_BOOK)
        await bot.state_dispenser.get(PhoneBookStates.phone_book_menu)

    elif ctx.get('phone_group') == 'Кафедры':
        await message.answer("Военный учебный центр: \n"
                             "8(499)267-39-51 доб. неизвестен\n"
                             "email: vk@miigaik.ru\n"
                             "каб. 256\n\n"
                             "Кафедра архитектурного проектирования:\n"
                             "8(499)267-39-51 доб. неизвестен\n"
                             "email: kap@miigaik.ru\n"
                             "каб. 603\n\n"
                             "Кафедра архитектуры и ландшафта:\n"
                             "8(499)404-12-20 доб. 3611\n"
                             "email: ail@miigaik.ru\n\n"
                             "Кафедра астрономии и космической геодезии:\n"
                             "8(499)267-57-62 доб. 3111\n"
                             "email: vikrylov@miigaik.ru\n"
                             "каб. 326 к. 6\n\n"
                             "Кафедра аэрокосмических съёмок:\n"
                             "каб. 426\n\n"
                             "Кафедра визуализации геоданных и картографического дизайна:\n"
                             "8(499)404-12-20 доб. 3232\n"
                             "email: giok@miigaik.ru\n"
                             "каб. 54 к. 1А\n\n"
                             "Кафедра высшей геодезии:\n"
                             "Нет информации\n\n"
                             "Кафедра высшей математики:\n"
                             "8(499)404-12-20 доб. 3131\n"
                             "email: yuney@miigaik.ru\n"
                             "каб. 409а\n\n"
                             "Кафедра географии:\n"
                             "8(499)404-12-20 доб. 3211\n"
                             "email: kg@miigaik.ru\n"
                             "каб. 413\n\n"
                             "Кафедра геодезии:\n"
                             "8(499)404-12-20 доб. 3541\n"
                             "email: oznamec@miigaik.ru\n"
                             "каб. 14 к. 1А\n\n"
                             "Кафедра геоинформационных систем и технологий:\n"
                             "8(499)404-12-20 доб. 3321\n"
                             "email: zhurkin@miigaik.ru\n"
                             "4 этаж, над кафедрой физ. воспитания\n\n"
                             "Кафедра градостроительства:\n"
                             "email: snejinskaya@feut.ru\n"
                             "каб. 206 к. 2\n\n"
                             "Кафедра гражданского права и процесса:\n"
                             "8(499)404-12-20 доб. 3651\n"
                             "email: gpp@miigaik.ru\n"
                             "каб. 421\n\n"
                             "Кафедра земельного права и государственной регистрации недвижимости:\n"
                             "8(499404-12-20 доб. 3691\n"
                             "email: zgigrp@miigaik.ru \n"
                             "каб. 55 к. 1А\n\n"
                             "Кафедра землеустройства и кадастров:\n"
                             "Нет информации\n\n"
                             "Кафедра информационно-измерительных систем:\n"
                             "8(499)261-85-64 доб. 1001\n"
                             "email: maiorov@miigaik.ru\n"
                             "каб. 6 к. 3\n\n"
                             "Кафедра истории, философии и социальных наук:\n"
                             "8(499)404-12-20 доб. 3641\n"
                             "email: emchenko@miigaik.ru\n"
                             "каб. 41к. 1А\n\n"
                             "Кафедра картографии:\n"
                             "8(499)404-12-20 доб. 3241\n"
                             "email: cartography@miigaik.ru\n"
                             "каб. 519\n\n"
                             "Кафедра космического мониторинга и экологии:\n"
                             "8(499)404-12-20 доб. 3331\n"
                             "email: pe@miigaik.ru\n"
                             "каб. 553\n\n"
                             "Кафедра лингвистики:\n"
                             "8(499)404-12-20 доб. 3661\n"
                             "email: transcript@miigaik.ru\n"
                             "каб. 434\n\n"
                             "Кафедра оптико-электронных приборов:\n"
                             "каб. 48а к. 1А\n\n"
                             "Кафедра прикладной геодезии:\n"
                             "8(499)404-12-20 доб. 3140\n"
                             "email: gnss@miigaik.ru\n"
                             "каб. 121 к. 1А\n\n"
                             "Кафедра прикладной информатики:\n"
                             "8(499)404-12-20 доб. 5435\n"
                             "email: dd_uchaev@edu.miigaik.ru\n\n"
                             "Кафедра прикладной оптики:\n"
                             "8(499)404-12-20 доб. 3432\n"
                             "email: kafedra-po@yandex.ru\n"
                             "каб. 1 к. 1А\n\n"
                             "Кафедра проектирования оптических приборов:\n"
                             "8(499)404-12-20 доб. 3441\n"
                             "email: parvulusov@miigaik.ru\n"
                             "каб. 416\n\n"
                             "Кафедра уголовного права и процесса:\n"
                             "8(499)263-29-79 доб. 3671\n"
                             "email: tpiupd@miigaik.ru\n"
                             "каб. 410а\n\n"
                             "Кафедра управления недвижимостью и развитием территорий:\n"
                             "8(499)404-12-20 доб. 1612\n"
                             "email: a_tararin@edu.miigaik.ru\n"
                             "каб. 155\n\n"
                             "Кафедра физики:\n"
                             "8(499)404-12-20 доб. 3451\n"
                             "email: fizika@miigaik.ru\n\n"
                             "Кафедра физического воспитания:\n"
                             "8(499)404-12-20 доб. 3681\n"
                             "email: miigaiksport@ya.ru\n"
                             "каб. 363\n\n"
                             "Кафедра фотограмметрии:\n"
                             "8(499)404-12-20 доб. 3342\n"
                             "email: fot@miigaik.ru\n\n"
                             "Кафедра цифровой картографии:\n"
                             "8(499)177-50-00 доб. 15004\n"
                             "email: brovko.priroda@mail.ru\n\n"
                             "Кафедра экономики:\n"
                             "8(499)404-12-20 доб. 3541\n"
                             "email: m_zabaeva@miigaik.ru\n"
                             "каб. 501 к. 2")
        await message.answer("Если вы точно уверены, что какой-либо из контактов неверен, используйте функцию "
                             "предложить исправление.", keyboard=KEYBOARD_PHONE_BOOK)
        await bot.state_dispenser.get(PhoneBookStates.phone_book_menu)
    elif ctx.get('phone_group') == 'Иное':
        await message.answer("Общежитие «Дом студентов»:\n"
                             "Дегавцова Ольга Александровна, 8(499)261-81-66 доб. 6521\n"
                             "email: ds@miigaik.ru\n"
                             "корп.4, эт.1, каб.3А\n\n"
                             "Общежитие «Дорогомилово»:\n"
                             "Брейнак Марина Петровна, 8(499)249-16-22 доб. 6571\n"
                             "email: do@miigaik.ru\n"
                             "эт.1, каб.245\n\n"
                             "Планово-финансовое управление:\n"
                             "8(499)267-25-54 доб. 4131\n"
                             "email: pfu@miigaik.ru\n"
                             "каб. 343\n\n"
                             "Служба социального обеспечения:\n"
                             "8(499)261-09-84 доб. 4109\n"
                             "email: juridicalservice155@gmail.com\n"
                             "каб. 355 \n\n")
        await message.answer("Если вы точно уверены, что какой-либо из контактов неверен, используйте функцию "
                             "предложить исправление.", keyboard=KEYBOARD_PHONE_BOOK)
        await bot.state_dispenser.get(PhoneBookStates.phone_book_menu)
    elif ctx.get('phone_group') == 'Назад':
        await message.answer("Возвращаемся...", keyboard=KEYBOARD_ADDITIONAL_MENU)
        await bot.state_dispenser.set(message.peer_id, state=AdditionalMenuStates.main)


class DoNotAnswer(vkbottle.BaseStateGroup):
    stop = 0


@bot.on.private_message(text='!игнор')
async def do_not_answer(message: Message):
    await bot.state_dispenser.set(message.peer_id, DoNotAnswer.stop)
    await message.answer("Введите !продолжить для возвращения к боту")


@bot.on.private_message(state=DoNotAnswer.stop)
async def do_not_answer(message: Message):
    ctx.set('do_not_answer', message.text)
    if ctx.get('do_not_answer') == '!продолжить':
        await message.answer('Возобновляю работу', keyboard=KEYBOARD_MAIN_MENU)
        await bot.state_dispenser.delete(message.peer_id)
    elif ctx.get('do_not_answer') != '!продолжить':
        await bot.state_dispenser.get(DoNotAnswer.stop)


@bot.on.private_message()
async def unknown_command(message: Message):
    await message.answer("Я вас не понимаю. Воспользуйтесь меню.", keyboard=KEYBOARD_MAIN_MENU)


conn.commit()
bot.run_forever()
