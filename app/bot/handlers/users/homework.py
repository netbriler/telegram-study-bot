import calendar
from datetime import datetime, timedelta

from telebot.types import Message, CallbackQuery

from app.models import Task
from app.services.tasks import get_tasks_by_week
from ...base import base, callback_query_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_week_inline_markup
from ...loader import bot, bot_username


@bot.message_handler(regexp='^📝 Домашнее задание$')
@bot.message_handler(commands=['homework'])
@base()
def homework_handler(message: Message):
    text, markup = _get_homework_data()

    send_message_private(message, text, reply_markup=markup, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('homework'))
@callback_query_base()
def inline_homework_handler(call: CallbackQuery):
    query, option = call.data.split('_')
    if option == 'this':
        date = datetime.today()
    elif option == 'next':
        date = datetime.today() + timedelta(weeks=1)
    else:
        return

    timetable = get_tasks_by_week(date.isocalendar()[1])

    text = _get_text(timetable)
    if not call.inline_message_id and call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_week_inline_markup(query, option == 'next')
    try:
        if call.inline_message_id:
            bot.edit_message_text(text, message_id=call.inline_message_id, inline_message_id=call.inline_message_id,
                                  reply_markup=markup,
                                  disable_web_page_preview=True)
        else:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup,
                                  disable_web_page_preview=True)
        bot.answer_callback_query(call.id, 'Ок')
    except Exception as e:
        if e.error_code == 400:
            bot.answer_callback_query(call.id, 'Ничего не поменялось')


def _get_text(timetable: list[list[Task]]):
    deep_link = f'tg://resolve?domain={bot_username}&start=task'

    text = ''
    for i in range(len(timetable)):
        tasks = timetable[i]
        if not tasks:
            continue

        text += calendar.day_name[i].capitalize() + ':\n'

        j = 1
        for task in tasks:
            if task.subject:
                text += f'{j}) <b>{task.subject.name}<a href="{deep_link}{task.id}">⠀</a></b>\n{task.text.rstrip()}\n\n'
                j += 1

        text = text.rstrip() + '\n\n'

    text = text.rstrip()

    if not text:
        return 'Нет домашних заданий'

    return text


def _get_homework_data():
    next_week = False

    now = datetime.now()
    if now.weekday() > 4 or (now.weekday() == 4 and now.hour > 13):
        next_week = True
        now += timedelta(weeks=1)

    timetable = get_tasks_by_week(now.isocalendar()[1])

    text = _get_text(timetable)

    markup = get_week_inline_markup('homework', next_week)

    return text, markup
