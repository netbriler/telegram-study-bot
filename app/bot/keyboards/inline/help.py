from flask import url_for
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_help_inline_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    markup.row(InlineKeyboardButton(text='👑 Админ панель', url=url_for('main.login')))
    return markup
