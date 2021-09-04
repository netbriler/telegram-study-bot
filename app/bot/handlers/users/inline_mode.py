from telebot.types import InlineQueryResultArticle, InlineQuery, InputTextMessageContent

from telebot.types import InlineQueryResultArticle, InlineQuery, InputTextMessageContent

from app.utils.helper import generate_inline_id
from .homework import _get_homework_data
from .today_homework import _get_today_homework_data
from .schedule import _get_schedule_data
from .current_info import _get_current_info_data
from ...loader import bot


@bot.inline_handler(lambda q: True)
def inline_echo(inline_query: InlineQuery):
    schedule_text, schedule_markup = _get_schedule_data()

    schedule = InlineQueryResultArticle(
        id=generate_inline_id('schedule'),
        title=f'Расписание',
        description='Узнать расписание',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/1f4c3.png',
        input_message_content=InputTextMessageContent(schedule_text, parse_mode='HTML'),
        reply_markup=schedule_markup
    )

    homework_text, homework_markup = _get_homework_data()

    homework = InlineQueryResultArticle(
        id=generate_inline_id('homework'),
        title=f'Домашнее задание',
        description='Узнать домашнее задание',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/1f4dd.png',
        input_message_content=InputTextMessageContent(homework_text, parse_mode='HTML'),
        reply_markup=homework_markup
    )
    
    today_homework_text, today_homework_markup = _get_today_homework_data()

    today_homework = InlineQueryResultArticle(
        id=generate_inline_id('today_homework'),
        title=f'Домашнее задание заданое сегодня',
        description='Узнать домашнее задание, которое задали сегодня',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/1f4dd.png',
        input_message_content=InputTextMessageContent(today_homework_text, parse_mode='HTML'),
        reply_markup=today_homework_markup
    )
    
    current_info_text, current_info_markup = _get_current_info_data()

    current_info = InlineQueryResultArticle(
        id=generate_inline_id('current_info'),
        title=f'Какая сейчас пара',
        description='Определить, сколько времени осталось до конца пары и какая пара будет следующая',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/2753.png',
        input_message_content=InputTextMessageContent(current_info_text, parse_mode='HTML'),
        reply_markup=current_info_markup
    )

    bot.answer_inline_query(inline_query.id, results=[schedule, homework, today_homework, current_info], cache_time=1)
