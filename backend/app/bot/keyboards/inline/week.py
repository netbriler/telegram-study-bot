import telebot
from telebot import types


def get_week_inline_markup(query: str, next: bool = False):
    markup = types.InlineKeyboardMarkup()
    this = 'На эту неделю' + ('*' if not next else '')
    next = 'На следущую неделю' + ('*' if next else '')
    markup.row(types.InlineKeyboardButton(this, callback_data=query + '_this'))
    markup.row(types.InlineKeyboardButton(next, callback_data=query + '_next'))
    return markup
