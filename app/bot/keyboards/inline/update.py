from telebot import types


def get_update_inline_markup(query: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('🔄Обновить🔄', callback_data=f'{query}_update'))
    return markup
