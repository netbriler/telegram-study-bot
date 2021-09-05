from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models import File


def get_files_inline_markup(files: list[File], inline: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for file in files:
        if inline:
            markup.row(InlineKeyboardButton(file.title, switch_inline_query_current_chat=f'file{file.id}'))
        else:
            markup.row(InlineKeyboardButton(file.title, callback_data=f'file_{file.id}'))

    return markup
