import random

from app.models import User
from app.utils.profanity_filter import ProfanityFilter
from telebot.types import Message, CallbackQuery

from ...base import base, callback_query_base
from ...loader import bot
from ...utils import send_message_private


@bot.message_handler(content_types=['text'], func=lambda m: True)
@base(send_chat_action=False)
def get_all_messages(message: Message, current_user: User):
    pf = ProfanityFilter()

    answer_list = ['Фу! Как некультурно!', 'Мат - для лохов', 'Не матюкайся', 'Не матерись',
                   'Мне показалось, или ты быканул?', 'Мат - плохо', 'Не матерись дуралей',
                   'Не излагай свои мысли как прибей', 'Кто обзывается, тот сам так и называется']

    if pf.is_profane(message.text):
        send_message_private(message, random.choice(answer_list), reply_to_message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: True)
@callback_query_base()
def get_all_callback_queries(call: CallbackQuery, current_user: User):
    pass
