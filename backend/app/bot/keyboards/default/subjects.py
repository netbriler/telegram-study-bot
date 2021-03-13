from app.services.subjects import get_all_subjects
from telebot import types


def get_subjects_keyboard_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    subjects = get_all_subjects()
    for s in range(int(len(subjects) / 2)):
        s *= 2
        btn = types.KeyboardButton(subjects[s].name)
        btn2 = types.KeyboardButton(subjects[s + 1].name)
        markup.row(btn, btn2)
    if len(subjects) % 2:
        markup.add(types.KeyboardButton(subjects[-1].name))
    markup.add(types.KeyboardButton('❌Отменить❌'))
    return markup
