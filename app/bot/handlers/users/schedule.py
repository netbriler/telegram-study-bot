import calendar
from datetime import datetime, timedelta

from telebot.types import Message, CallbackQuery

from app.models import Subject
from app.services.timetable import get_subjects_by_week
from ...base import base, callback_query_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_week_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^📃Расписание📃$')
@bot.message_handler(commands=['schedule'])
@base()
def schedule_handler(message: Message):
    # set next week markup
    next_week = False

    now = datetime.now()
    if now.weekday() > 4 or (now.weekday() == 4 and now.hour > 13):
        next_week = True
        now += timedelta(weeks=1)

    timetable = get_subjects_by_week(now.isocalendar()[1])

    text = _get_text(timetable)

    markup = get_week_inline_markup('schedule', next_week)
    send_message_private(message, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule'))
@callback_query_base()
def inline_schedule_handler(call: CallbackQuery):
    query, option = call.data.split('_')
    if option == 'this':
        date = datetime.today()
    elif option == 'next':
        date = datetime.today() + timedelta(weeks=1)
    else:
        return

    next = option == 'next'

    timetable = get_subjects_by_week(date.isocalendar()[1])

    text = _get_text(timetable)
    if call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_week_inline_markup(query, next)

    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup,
                              disable_web_page_preview=True)
    except Exception as e:
        if e.error_code == 400:
            bot.answer_callback_query(call.id, 'Ничего не поменялось')


def _get_text(timetable: list[list[Subject]]):
    text = ''
    for i in range(len(timetable)):
        subjects = timetable[i]
        if not subjects:
            continue

        text += calendar.day_name[i].capitalize() + ':\n'

        for j in range(len(subjects)):
            text += f'{j + 1}) <b>{subjects[j].name}</b> (<i>{subjects[j].audience}</i>)\n'

        text += '\n'

    if not text:
        return 'Нет расписания'

    return text

