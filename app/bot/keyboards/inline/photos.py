from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_photos_inline_markup(query: str, id: int, markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    if not markup:
        markup = InlineKeyboardMarkup(row_width=2)

    query = query + str(id)

    markup.row(InlineKeyboardButton('Посмотреть прикрепленные фотографии', callback_data=f'{query}_photos'))

    return markup


def get_delete_photo_inline_markup(query: str, id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    query = query + str(id)

    markup.row(InlineKeyboardButton('☢ Удалить', callback_data=f'{query}_delete'))
    markup.row(InlineKeyboardButton('❌ Отменить', callback_data=f'{query}_cancel'))

    return markup

