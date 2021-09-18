from html import escape
from math import ceil

from telebot.types import Message, CallbackQuery, InputMediaPhoto

from app.models import User
from app.services.tasks import edit_task, get_active_tasks, get_task, delete_task
from .add_file import get_file_handler
from ...base import base, callback_query_base
from ...helpers import send_message_private, send_message_inline_private
from ...keyboards.default import get_menu_keyboard_markup, get_cancel_keyboard_markup
from ...keyboards.inline import get_edit_inline_markup, get_files_inline_markup, get_photos_inline_markup
from ...loader import bot, bot_username


@bot.message_handler(regexp='^✏ Редактировать$')
@bot.message_handler(commands=['edit'])
@base(is_admin=True)
def edit_tasks_handler(message: Message):
    text = 'Домашнее задание:\n'

    tasks = get_active_tasks()

    i = 1
    for task in tasks:
        task_text = (task.text[:75] + '..') if len(task.text) > 75 else task.text
        text += f'{i}) <b>{task.subject.name}</b>\n{task_text} /edit{task.id}\n\n'
        i += 1

    bot.send_message(message.chat.id, text, disable_web_page_preview=True)


@bot.message_handler(regexp=f'^/edit\\d+(@{bot_username})?$')
@base(is_admin=True)
def get_edit_task_handler(message: Message):
    id = int(message.text[5:].replace(f'@{bot_username}', '').strip())

    send_task_edit_menu(message, id)


@bot.message_handler(commands=['start'], func=lambda m: m.text.startswith('/start task'))
@base()
def deep_link_edit_handler(message: Message, current_user: User):
    id = int(message.text[11:])

    send_task_edit_menu(message, id, current_user.is_admin())


@bot.callback_query_handler(func=lambda call: call.data.startswith('task'))
@callback_query_base(is_admin=True)
def inline_task_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    query, option = call.data.split('_')
    id = int(query[4:])

    if option == 'cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return bot.delete_message(chat_id, message_id)

    task = get_task(id)
    if not task:
        bot.answer_callback_query(call.id, 'Задание уже удалено', show_alert=True)
        return bot.delete_message(chat_id, message_id)

    if option == 'edit':
        text = (f'Введите измененное задание для предмета:\n<b>{task.subject.name}</b>\n'
                f'<pre>{task.text}</pre>')

        markup = get_cancel_keyboard_markup()
        response = send_message_inline_private(call, text, reply_markup=markup)
        bot.register_next_step_handler(response, edit_task_handler, id=id)

        bot.delete_message(chat_id, message_id)
    if option == 'files':
        text = 'Отправте файл для задания'

        response = send_message_private(call.message, text, reply_markup=get_cancel_keyboard_markup())
        bot.register_next_step_handler(response, get_file_handler, _task=task.to_json())
    if option == 'photos':
        if len(task.photos) < 1:
            return send_message_private(call.message, 'Нет фотографий')
        elif len(task.photos) < 11:
            media = [InputMediaPhoto(p.file_id) for p in task.photos]

            bot.answer_callback_query(call.id, 'Загружаю...')
            bot.send_chat_action(chat_id, 'upload_photo')

            return bot.send_media_group(chat_id, media)

        bot.answer_callback_query(call.id, 'Загружаю...')
        bot.send_chat_action(chat_id, 'upload_photo')

        i = 0
        for _ in range(ceil(len(task.photos) / 10)):
            media = [InputMediaPhoto(p.file_id) for p in task.photos[i:i+10]]

            bot.send_media_group(chat_id, media)

            i += 10
    elif option == 'delete':
        delete_task(id)
        bot.answer_callback_query(call.id, 'Удаленно', show_alert=True)
        bot.delete_message(chat_id, message_id)
    else:
        bot.answer_callback_query(call.id, 'Отменено', show_alert=True)
        bot.delete_message(chat_id, message_id)


@base(is_admin=True)
def edit_task_handler(message: Message, id: int, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно задание для предмета!')
        return bot.register_next_step_handler(response, edit_task_handler, id=id, current_user=current_user)

    task = edit_task(id, escape(message.text))

    text = 'Задание изменено ✅'

    markup = get_menu_keyboard_markup(current_user.is_admin())
    send_message_private(message, text, reply_markup=markup)

    send_task_edit_menu(message, task.id, current_user.is_admin())


def send_task_edit_menu(message: Message, id: int, allow_editing: bool = True):
    task = get_task(id)

    if not task:
        return send_message_private(message, f'Задание с id <b>{id}</b> не найдено', reply_to_message_id=message.id)

    text = (f'<b>{task.subject.name}</b>\n'
            f'Задано на: <i>{task.date}</i>\n'
            f'Добавлено: <i>{task.created_at}</i>\n\n'
            f'Текст задания:\n<pre>{task.text.strip()}</pre>')

    markup = None

    if task.files or task.photos:
        text += '\n\nСписок документов 👇'

    if task.photos:
        markup = get_photos_inline_markup('task', id, markup=markup)

    markup = get_files_inline_markup(task.files, markup=markup)

    if allow_editing:
        markup = get_edit_inline_markup('task', id, markup=markup, files_button=True)

    send_message_private(message, text, reply_markup=markup, disable_web_page_preview=True)
