from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_week_inline_markup(query: str, next: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    this_week_title = 'На эту неделю' + ('*' if not next else '')
    next_week_title = 'На следущую неделю' + ('*' if next else '')

    markup.row(InlineKeyboardButton(this_week_title, callback_data=f'{query}_this'))
    markup.row(InlineKeyboardButton(next_week_title, callback_data=f'{query}_next'))
    return markup
