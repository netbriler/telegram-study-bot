import telebot
from telebot import types

from app.services.subjects import get_all_subjects


def get_subjects_inline_markup(query: str):
    markup = types.InlineKeyboardMarkup()
    subjects = get_all_subjects()
    for s in range(int(len(subjects) / 2)):
        s *= 2
        btn = types.InlineKeyboardButton(subjects[s].name, callback_data=query + '_' + subjects[s].codename)
        btn2 = types.InlineKeyboardButton(subjects[s + 1].name, callback_data=query + '_' + subjects[s + 1].codename)
        markup.row(btn, btn2)
    if len(subjects) % 2:
        markup.add(types.InlineKeyboardButton(subjects[-1].name, callback_data=query + '_' + subjects[-1].codename))
    markup.row(types.InlineKeyboardButton('❌Отменить❌', callback_data=query + '_cancel'))
    return markup
