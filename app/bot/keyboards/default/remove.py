from telebot.types import ReplyKeyboardRemove


def get_remove_keyboard_markup() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove(selective=True)
