from flask import url_for
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl


def get_help_inline_markup(is_admin: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    if is_admin:
        login_url = LoginUrl(url_for('main.login_redirect', _external=True), request_write_access=True)
        markup.row(InlineKeyboardButton(text='👑 Админ панель', login_url=login_url))

    markup.row(InlineKeyboardButton(text='🤖 Встроить бота', switch_inline_query=''))

    return markup
