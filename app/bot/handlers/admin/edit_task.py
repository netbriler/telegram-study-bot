from html import escape

from telebot.types import Message, CallbackQuery

from app.models import User
from app.services.tasks import edit_task, get_active_tasks, get_task, delete_task
from ...base import base, callback_query_base
from ...helpers import send_message_private, send_message_inline_private
from ...keyboards.default import get_menu_keyboard_markup, get_cancel_keyboard_markup
from ...keyboards.inline import get_edit_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^🛠 Редактировать$')
@bot.message_handler(commands=['edit'])
@base(is_admin=True)
def edit_tasks_handler(message: Message):
    text = 'ДЗ:\n'

    tasks = get_active_tasks()

    i = 1
    for task in tasks:
        task_text = (task.text[:75] + '..') if len(task.text) > 75 else task.text
        text += f'{i}) <b>{task.subject.name}</b>\n{escape(task_text)} /edit{task.id}\n\n'
        i += 1

    bot.send_message(message.chat.id, text, disable_web_page_preview=True)


@bot.message_handler(regexp=f'^/edit\\d+(@{bot.get_me().username})?$')
@base(is_admin=True)
def get_edit_task_handler(message: Message):
    id = int(message.text[5:].replace(f'@{bot.get_me().username}', '').strip())
    task = get_task(id)

    if not task:
        return bot.reply_to(message, f'Задание с id <b>{id}</b> не найдено')

    text = f'{task.subject.name} - {escape(task.text)}'

    markup = get_edit_inline_markup('task', id)
    bot.send_message(message.chat.id, text, reply_markup=markup, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('task'))
@callback_query_base(is_admin=True)
def inline_edit_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    query, option = call.data.split('_')
    id = int(query[4:])

    task = get_task(id)
    if not task:
        bot.answer_callback_query(call.id, 'Задание уже удалено')
        bot.delete_message(chat_id, message_id)

    if option == 'edit':
        text = ('Введите измененное задание:\n'
                f'{task.subject.name} - <pre>{task.text}</pre>')

        markup = get_cancel_keyboard_markup()
        response = send_message_inline_private(call, text, reply_markup=markup)
        bot.register_next_step_handler(response, edit_task_handler, id=id)

        bot.delete_message(chat_id, message_id)
    elif option == 'delete':
        delete_task(id)
        bot.answer_callback_query(call.id, 'Удаленно')
        bot.delete_message(chat_id, message_id)
    else:
        bot.answer_callback_query(call.id, 'Отменено')
        bot.delete_message(chat_id, message_id)


@base(is_admin=True)
def edit_task_handler(message: Message, id: int, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно задание для предмета!')
        return bot.register_next_step_handler(response, edit_task_handler, id=id, current_user=current_user)

    task = edit_task(id, message.text)

    text = ('Изменено:\n'
            f'{task.subject.name} - {escape(task.text)}')

    markup = get_menu_keyboard_markup(current_user.is_admin())
    send_message_private(message, text, reply_markup=markup)
