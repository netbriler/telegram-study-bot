import calendar
from datetime import datetime, timedelta

from telebot.types import Message, CallbackQuery

from app.models import Subject
from app.services.timetable import get_subjects_by_week
from ...base import base, callback_query_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_week_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^📃 Расписание$')
@bot.message_handler(commands=['schedule'])
@base()
def schedule_handler(message: Message):
    text, markup = _get_schedule_data()

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

    timetable = get_subjects_by_week(date.isocalendar()[1])

    text = _get_text(timetable)
    if not call.inline_message_id and call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_week_inline_markup(query, option)

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
            bot.answer_callback_query(call.id, 'Ничего не поменялось', show_alert=True)


def _get_text(timetable: list[list[Subject]]):
    text = ''
    for i in range(len(timetable)):
        subjects = timetable[i]
        if not subjects:
            continue

        text += calendar.day_name[i].capitalize() + ':\n'

        for j in range(len(subjects)):
            text_audience = ''
            if subjects[j].audience:
                text_audience = f'(<i>{subjects[j].audience}</i>)'

            text += f'{j + 1}) <b>{subjects[j].name}</b> {text_audience}\n'

        text += '\n'

    if not text:
        return '⚠ Нет расписания'

    return text


def _get_schedule_data():
    shift = 'this'

    now = datetime.now()
    if now.weekday() > 4 or (now.weekday() == 4 and now.hour > 13):
        shift = 'next'
        now += timedelta(weeks=1)

    timetable = get_subjects_by_week(now.isocalendar()[1])

    text = _get_text(timetable)

    markup = get_week_inline_markup('schedule', shift)
    return text, markup
