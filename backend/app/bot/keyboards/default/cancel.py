from telebot import types


def get_cancel_keyboard_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(types.KeyboardButton('❌Отменить❌'))
    return markup
