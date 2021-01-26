import humanize

from math import floor
from datetime import datetime, date, timedelta, time
from telebot.types import Message, CallbackQuery

from ...loader import bot, current_app, DIR
from ...base import base, callback_query_base
from ...keyboards.inline import get_update_inline_markup
from ...utils import send_message_private

from app.models import User

from app.services.timetable import get_subjects_by_date


@bot.message_handler(commands=['current_info'])
@base()
def current_info_handler(message: Message, current_user: User):
    text = _get_text()

    send_message_private(message, text, reply_markup=get_update_inline_markup('current_info'))


@bot.callback_query_handler(func=lambda call: call.data.startswith('current_info'))
@callback_query_base()
def inline_homework_handler(call: CallbackQuery, current_user: User):
    query, option = call.data.split('current_info_')
    if option == 'update':
        text = _get_text()

        if call.message.chat.type != 'private':
            text += f'<a href="tg://user?id={call.from_user.id}">⠀</a>'

        chat_id = call.message.chat.id
        message_id = call.message.message_id

        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=get_update_inline_markup('current_info'))
        except Exception as e:
            if e.error_code == 400:
                bot.answer_callback_query(call.id, 'Ничего не поменялось')


def _get_text():
    text = ''
    current_datetime = datetime.now()
    subjects = get_subjects_by_date(current_datetime.date())
    checking_datetime = datetime.combine(date.today(), time(8, 30))

    humanize.i18n.activate(current_app.config['LOCATE'])

    if current_datetime < checking_datetime:
        time_to_end = checking_datetime - current_datetime
        humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes')

        text = f'До первой пары осталось еще <b>{humanize_time_to_end}</b>'

        return text

    for i in range(len(subjects)):
        if checking_datetime < current_datetime < checking_datetime + timedelta(minutes=75):
            time_to_end = (checking_datetime + timedelta(minutes=75)) - current_datetime
            humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes', format='%0.0f')

            text = (f'Сейчас: <b>{subjects[i].name}</b>\n'
                    f'До конца еще <b>{humanize_time_to_end}</b>\n\n')

            if i < len(subjects) - 1:
                text += f'Следующая пара: <b>{subjects[i + 1].name}</b>'

            break

        checking_datetime += timedelta(minutes=75)
        if i == len(subjects) - 1:
            break
        if checking_datetime < current_datetime < checking_datetime + timedelta(minutes=10):
            time_to_end = (checking_datetime + timedelta(minutes=10)) - current_datetime
            humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes', format='%0.0f')

            text = ('Сейчас перемена\n'
                    f'До конца еще <b>{humanize_time_to_end}</b>\n\n'
                    f'Следующая пара: <b>{subjects[i+1].name}</b>')

            break
        checking_datetime += timedelta(minutes=10)

    if text == '':
        text = 'Сегодня пар больше не будет'

    return text.rstrip()

