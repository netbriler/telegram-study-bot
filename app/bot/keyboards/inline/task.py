from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_edit_inline_markup(query: str, id: int, markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    if not markup:
        markup = InlineKeyboardMarkup()

    query = query + str(id)

    markup.row(InlineKeyboardButton('✏ Редактировать', callback_data=f'{query}_edit'),
               InlineKeyboardButton('☢ Удалить', callback_data=f'{query}_delete'))

    markup.row(InlineKeyboardButton('❌ Отменить', callback_data=f'{query}_cancel'))
    return markup
