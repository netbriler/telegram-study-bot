from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models import Subject
from app.services.subjects import get_all_subjects


def get_subjects_inline_markup(query: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    subjects = get_all_subjects()
    subjects_button_list = [
        InlineKeyboardButton(subject.name, callback_data=f'{query}_{subject.codename}') for subject in subjects]

    markup.add(*subjects_button_list)

    markup.row(InlineKeyboardButton('❌ Отменить', callback_data=f'{query}_cancel'))
    return markup
