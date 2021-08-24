from flask import url_for
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl


def get_help_inline_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    login_url = LoginUrl(url_for('main.login_redirect', _external=True), request_write_access=True)

    markup.row(InlineKeyboardButton(text='👑 Админ панель', login_url=login_url))

    return markup
