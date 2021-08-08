from telebot.types import ReplyKeyboardMarkup


def get_menu_keyboard_markup(is_admin: bool = False) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    if is_admin:
        markup.add('➕Добавить➕', '🛠️Редактировать🛠️')

    markup.row('📃Расписание📃', '📝ДЗ📝')
    markup.row('🆘Помощь🆘')
    markup.row('👀Информация👀')
    return markup
