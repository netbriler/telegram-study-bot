import calendar
from datetime import datetime, timedelta

from telebot.types import Message, CallbackQuery
from app.bot.loader import bot

from app.bot.base import base, callback_query_base

from app.models import User

from app.services.tasks import get_tasks_by_week

from app.bot.keyboards.inline import get_week_inline_markup


@bot.message_handler(regexp='^📝ДЗ📝$')
@bot.message_handler(commands=['homework'])
@base()
def send_homework(message: Message, current_user: User):
    # set next week markup
    next = False

    now = datetime.now()
    if now.weekday() >= 4 and now.hour > 13:
        next = True
        now += timedelta(weeks=1)

    timetable = get_tasks_by_week(now.isocalendar()[1])

    text = _get_text(timetable)

    markup = get_week_inline_markup('homework', next)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('homework'))
@callback_query_base()
def inline_send_homework(call: CallbackQuery, current_user: User):
    query, option = call.data.split('_')
    if option == 'this':
        date = datetime.today()
    elif option == 'next':
        date = datetime.today() + timedelta(weeks=1)
    else:
        return

    next = option == 'next'

    markup = get_week_inline_markup(query, next)
    timetable = get_tasks_by_week(date.isocalendar()[1])

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    text = _get_text(timetable)
    bot.edit_message_text(text, chat_id, message_id, parse_mode='HTML', reply_markup=markup,
                          disable_web_page_preview=True)


def _get_text(timetable):
    text = 'ДЗ:\n'
    for i in range(len(timetable)):
        tasks = timetable[i]
        text += calendar.day_name[i].capitalize() + ':\n'

        j = 1
        for task in tasks:
            text += f'{j}) {task.subject.name} - {task.text}\n'
            j += 1

        text += '\n'

    return text

