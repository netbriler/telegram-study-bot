from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_week_inline_markup(query: str, shift: str = 'this', with_previous: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    this_week_title = 'На эту неделю' + ('*' if shift == 'this' else '')
    next_week_title = 'На следущую неделю' + ('*' if shift == 'next' else '')

    if with_previous:
        previous_week_title = 'За прошлую неделю' + ('*' if shift == 'previous' else '')
        markup.row(InlineKeyboardButton(previous_week_title, callback_data=f'{query}_previous'))

    markup.row(InlineKeyboardButton(this_week_title, callback_data=f'{query}_this'))
    markup.row(InlineKeyboardButton(next_week_title, callback_data=f'{query}_next'))
    return markup
