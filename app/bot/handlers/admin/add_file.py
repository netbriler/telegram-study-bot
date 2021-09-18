from html import escape

from telebot.types import Message

from app.models import User
from app.services.files import add_file
from app.services.photos import add_photos
from app.services.subjects import recognize_subject
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_subjects_keyboard_markup, get_cancel_keyboard_markup, get_menu_keyboard_markup, \
    get_enough_keyboard_markup
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


@bot.message_handler(content_types=['photo'],
                     func=lambda m: f'{m.chat.id}:task_for_add_photos_id' in bot.next_step_backend.handlers)
@base(is_admin=True)
def add_photo_to_task_handler(message: Message):
    bot.next_step_backend.handlers[f'{message.chat.id}:photos_to_add_list'].append(message.photo[-1].file_id)


@bot.message_handler(func=lambda m: f'{m.chat.id}:task_for_add_photos_id' in bot.next_step_backend.handlers)
@base()
def photos_to_add_list(message: Message, current_user):
    if not current_user.is_admin():
        bot.next_step_backend.handlers.pop(f'{message.chat.id}:task_for_add_photos_id', None)
        bot.next_step_backend.handlers.pop(f'{message.chat.id}:photos_to_add_list', None)
        return send_message_private(message, 'Ок 👍', reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    if message.content_type == 'text':
        if message.text == '👀 Достаточно':
            task_id = bot.next_step_backend.handlers[f'{message.chat.id}:task_for_add_photos_id']
            photos_to_add = bot.next_step_backend.handlers[f'{message.chat.id}:photos_to_add_list']

            add_photos(photos_to_add, task_id)

            send_message_private(message, 'Фотографии добавлен ✅',
                                 reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
        else:
            send_message_private(message, 'Ок 👍', reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

        bot.next_step_backend.handlers.pop(f'{message.chat.id}:task_for_add_photos_id', None)
        bot.next_step_backend.handlers.pop(f'{message.chat.id}:photos_to_add_list', None)

    else:
        return bot.reply_to(message, f'Это {message.content_type}, а мне нужена фотография!')


@base(is_admin=True)
def get_file_handler(message: Message, subject: dict = None, _task: dict = None):
    if _task and message.content_type == 'photo':
        bot.next_step_backend.handlers[f'{message.chat.id}:task_for_add_photos_id'] = _task['id']
        bot.next_step_backend.handlers[f'{message.chat.id}:photos_to_add_list'] = []

        add_photo_to_task_handler(message)

        return send_message_private(message, 'Отправте все фото, после чего нажмине на кнопку 👇',
                                    reply_markup=get_enough_keyboard_markup())

    if message.content_type != 'document':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужен файл!')
        return bot.register_next_step_handler(response, get_file_handler, subject=subject, _task=_task)

    text = f'Напишите название для файла'

    response = bot.reply_to(message, text)
    bot.register_next_step_handler(response, add_file_handler, subject=subject, _task=_task,
                                   file_id=message.document.file_id)


@base(is_admin=True)
def add_file_handler(message: Message, subject: dict, _task: dict, file_id: str, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно название для файла!')
        return bot.register_next_step_handler(response, add_file_handler, subject=subject, _task=_task, file_id=file_id,
                                              current_user=current_user)

    if subject:
        file = add_file(escape(message.text), file_id, subject_codename=subject['codename'])
    elif _task:
        file = add_file(escape(message.text), file_id, task_id=_task['id'])
    else:
        return send_message_private(message, 'Ошибка при добавлении ❌',
                                    reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    send_message_private(message, 'Файл добавлен ✅', reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
