from telebot import types


def get_remove_keyboard_markup():
    return types.ReplyKeyboardRemove(selective=True)
