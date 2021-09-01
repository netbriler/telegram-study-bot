from html import escape

from telebot.types import Message

from app.models import User
from app.services.subjects import recognize_subject
from app.services.tasks import add_task
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_subjects_keyboard_markup, get_cancel_keyboard_markup, get_menu_keyboard_markup
from ...loader import bot


@bot.message_handler(regexp='^➕ Добавить$')
@bot.message_handler(commands=['add'])
@base(is_admin=True)
def add_task_handler(message: Message):
    text = 'Выберите предмет из меню 👇'

    response = send_message_private(message, text, reply_markup=get_subjects_keyboard_markup())

    bot.register_next_step_handler(response, get_subject_handler)


@base(is_admin=True)
def get_subject_handler(message: Message):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно название предмета!')
        return bot.register_next_step_handler(response, get_subject_handler)

    subject = recognize_subject(message.text)

    text = f'Напишите задание для предмета: {subject.name}'

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, add_task_handler, subject=subject.to_json())


@base(is_admin=True)
def add_task_handler(message: Message, subject: dict, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно задание для предмета!')
        return bot.register_next_step_handler(response, add_task_handler, subject=subject, current_user=current_user)

    task = add_task(subject['codename'], escape(message.text))
    if not task:
        return send_message_private(message,
                                    f'<b>Не удалось добавить задание!</b>\nПохоже предмета "<i>{subject["name"]}</i>" нет в расписании',
                                    reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    text = ('Добавлено:\n'
            f'{subject["name"]} - {task.text}')

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))


@bot.message_handler(regexp='^!(.+)-(.|\s)+$')
@base(is_admin=True)
def add_task_via_decorator_handler(message: Message, current_user: User):
    query = message.text.replace('!', '').strip()
    subject_name = query.split('-')[0]
    task_text = query.replace(subject_name, '', 1).replace('-', '', 1).strip()

    subject = recognize_subject(subject_name)

    task = add_task(subject.codename, escape(task_text))
    if not task:
        return send_message_private(message,
                                    f'<b>Не удалось добавить задание!</b>\nПохоже предмета "<i>{subject.name}</i>" нет в расписании',
                                    reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    text = ('Добавлено:\n'
            f'{subject.name} - {task.text}')

    bot.send_message(message.chat.id, text, parse_mode='HTML')
