from html import escape

from telebot.types import Message

from app.models import User
from app.services.files import add_file
from app.services.subjects import recognize_subject
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_subjects_keyboard_markup, get_cancel_keyboard_markup, get_menu_keyboard_markup
from ...loader import bot


@bot.message_handler(regexp='^📑 Добавить файл в информацию$')
@bot.message_handler(commands=['add_file'])
@base(is_admin=True)
def add_file_handler(message: Message):
    text = 'Выберите предмет для которого нужно добавить файл 👇'

    response = send_message_private(message, text, reply_markup=get_subjects_keyboard_markup())

    bot.register_next_step_handler(response, get_subject_handler)


@base(is_admin=True)
def get_subject_handler(message: Message):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно название предмета!')
        return bot.register_next_step_handler(response, get_subject_handler)

    subject = recognize_subject(message.text)

    text = f'Отправте файл для предмета {subject.name.lower()}'

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, get_file_handler, subject=subject.to_json())


@base(is_admin=True)
def get_file_handler(message: Message, subject: dict):
    if message.content_type != 'document':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужен файл!')
        return bot.register_next_step_handler(response, get_file_handler, subject=subject)

    text = f'Напишите название для файла'

    response = bot.reply_to(message, text)
    bot.register_next_step_handler(response, add_file_handler, subject=subject, file_id=message.document.file_id)


@base(is_admin=True)
def add_file_handler(message: Message, subject: dict, file_id: str, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно название для файла!')
        return bot.register_next_step_handler(response, add_file_handler, subject=subject, file_id=file_id,
                                              current_user=current_user)

    file = add_file(subject['codename'], escape(message.text), file_id)

    text = ('Добавлено:\n'
            f'{subject["name"]} - {file.title}')

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
