from html import escape

from app.models import User
from app.services.subjects import recognize_subject
from app.services.tasks import add_task
from telebot.types import Message

from ...base import base
from ...keyboards.default import get_subjects_keyboard_markup, get_cancel_keyboard_markup, get_remove_keyboard_markup
from ...loader import bot
from ...utils import send_message_private


@bot.message_handler(regexp='^➕Добавить➕$')
@bot.message_handler(commands=['add'])
@base(is_admin=True)
def add_task_handler(message: Message, current_user: User):
    text = 'Выберите предмет из меню 👇'

    response = send_message_private(message, text, reply_markup=get_subjects_keyboard_markup())

    bot.register_next_step_handler(response, get_subject_handler)


@base(is_admin=True)
def get_subject_handler(message: Message, current_user: User):
    subject = recognize_subject(message.text)

    text = 'Напишите задание для предмета: ' + subject.name

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, add_task_handler, subject)


@base(is_admin=True)
def add_task_handler(message: Message, current_user: User, subject):
    task = add_task(subject.codename, message.text)

    text = ('Добавлено:\n'
            f'{subject.name} - {escape(task.text)}')

    send_message_private(message, text, reply_markup=get_remove_keyboard_markup())


@bot.message_handler(regexp='^!.+-.+$')
@base(is_admin=True)
def add_task_via_decorator_handler(message: Message, current_user: User):
    query = message.text.replace('!', '').strip()
    subject_name = query.split('-')[0]
    task_text = query.replace(subject_name, '').replace('-', '').strip()

    subject = recognize_subject(subject_name)

    task = add_task(subject.codename, task_text)

    text = ('Добавлено:\n'
            f'{subject.name} - {escape(task.text)}')

    bot.send_message(message.chat.id, text, parse_mode='HTML')
