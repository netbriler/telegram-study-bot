from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models import File


def get_files_inline_markup(files: list[File], inline: bool = False,
                            markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    if not markup:
        markup = InlineKeyboardMarkup(row_width=2)

    if inline:
        files_button_list = [
            InlineKeyboardButton(file.title, switch_inline_query_current_chat=f'file{file.id}') for file in files]
    else:
        files_button_list = [
            InlineKeyboardButton(file.title, callback_data=f'file_{file.id}') for file in files]

    if files_button_list:
        markup.add(*files_button_list)

    return markup
