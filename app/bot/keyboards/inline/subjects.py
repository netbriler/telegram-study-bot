from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models import Subject
from app.services.subjects import get_all_subjects


def get_subjects_inline_markup(query: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    subjects = get_all_subjects()
    for s in range(int(len(subjects) / 2)):
        s *= 2
        markup.add(InlineKeyboardButton(subjects[s].name, callback_data=f'{query}_{subjects[s].codename}'),
                   InlineKeyboardButton(subjects[s + 1].name,
                                        callback_data=f'{query}_{subjects[s + 1].codename}'))

    if len(subjects) % 2:
        markup.add(InlineKeyboardButton(subjects[-1].name, callback_data=f'{query}_{subjects[-1].codename}'))

    markup.row(InlineKeyboardButton('❌ Отменить', callback_data=f'{query}_cancel'))
    return markup


def get_subject_files_inline_markup(subject: Subject) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    for file in subject.files:
        markup.row(InlineKeyboardButton(file.title, callback_data=f'file_{file.id}'))

    return markup
