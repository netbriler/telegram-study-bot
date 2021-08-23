from telebot.types import ReplyKeyboardMarkup


def get_cancel_keyboard_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('❌ Отменить')
    return markup
