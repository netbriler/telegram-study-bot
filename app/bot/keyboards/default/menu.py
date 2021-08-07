from telebot import types


def get_menu_keyboard_markup(is_admin=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if is_admin:
        add = types.KeyboardButton('➕Добавить➕')
        edit = types.KeyboardButton('🛠️Редактировать🛠️')
        markup.row(add, edit)
    schedule = types.KeyboardButton('📃Расписание📃')
    homework = types.KeyboardButton('📝ДЗ📝')
    helpme = types.KeyboardButton('🆘Помощь🆘')
    info = types.KeyboardButton('👀Информация👀')
    markup.row(schedule, homework)
    markup.row(helpme)
    markup.row(info)
    return markup
