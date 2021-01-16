import calendar
from datetime import datetime, timedelta

from telebot.types import Message, CallbackQuery

from ...loader import bot
from ...base import base, callback_query_base
from ...keyboards.inline import get_week_inline_markup

from app.models import User

from app.services.timetable import get_subjects_by_week


@bot.message_handler(regexp='^📃Расписание📃$')
@bot.message_handler(commands=['schedule'])
@base()
def schedule_handler(message: Message, current_user: User):
    # set next week markup
    next = False

    now = datetime.now()
    if now.weekday() > 4 or (now.weekday() == 4 and now.hour > 13):
        next = True
        now += timedelta(weeks=1)

    timetable = get_subjects_by_week(now.isocalendar()[1])

    text = _get_text(timetable)

    markup = get_week_inline_markup('schedule', next)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule'))
@callback_query_base()
def inline_schedule_handler(call: CallbackQuery, current_user: User):
    query, option = call.data.split('_')
    if option == 'this':
        date = datetime.today()
    elif option == 'next':
        date = datetime.today() + timedelta(weeks=1)
    else:
        return

    next = option == 'next'

    markup = get_week_inline_markup(query, next)
    timetable = get_subjects_by_week(date.isocalendar()[1])

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    text = _get_text(timetable)
    if call.message.chat.type != 'private':
        text = f'<a href="tg://user?id={call.from_user.id}">*</a>{text}'

    try:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, disable_web_page_preview=True)
    except Exception as e:
        if e.error_code == 400:
            bot.answer_callback_query(call.id, 'Ничего не поменялось')


def _get_text(timetable):
    text = 'Расписание:\n'
    for i in range(len(timetable)):
        subjects = timetable[i]
        text += calendar.day_name[i].capitalize() + ':\n'
        for j in range(len(subjects)):
            text += f'{j + 1}) {subjects[j].name}\n'

        text += '\n'

    return text
