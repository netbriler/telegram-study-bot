from telebot.types import ReplyKeyboardMarkup

from app.services.subjects import get_all_subjects


def get_subjects_keyboard_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
    subjects = get_all_subjects()

    names = list(map(lambda s: s.name, subjects))

    try:
        markup.add(names[0])
        markup.add(*names[1:5])
        markup.add(names[5])
        markup.add(*names[6:])
    except:
        pass

    markup.add('❌Отменить❌')
    return markup
