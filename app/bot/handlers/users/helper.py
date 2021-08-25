import random

from telebot.types import Message

from app.models import User
from app.utils.profanity_filter import ProfanityFilter
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_menu_keyboard_markup
from ...loader import bot, current_app


@bot.message_handler(content_types=['text'], func=lambda m: m.chat.type == 'private')
@base()
def _all_private_messages_handler(message: Message, current_user: User):
    text = 'Выберите действие в меню 👇'

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))


@bot.message_handler(content_types=['text'], func=lambda m: current_app.config['PROFANITY_FILTER'])
def _profanity_filter(message: Message):
    pf = ProfanityFilter()
    answer_list = ['Фу! Как некультурно!', 'Мат - для лохов', 'Не матюкайся', 'Не матерись',
                   'Мне показалось, или ты быканул?', 'Мат - плохо', 'Не матерись дуралей',
                   'Не излагай свои мысли как прибей', 'Кто обзывается, тот сам так и называется']

    if pf.is_profane(message.text):
        send_message_private(message, random.choice(answer_list), reply_to_message_id=message.message_id)