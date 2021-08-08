import random

from telebot.types import Message

from app.models import User
from app.utils.profanity_filter import ProfanityFilter
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_menu_keyboard_markup
from ...loader import bot


@bot.message_handler(content_types=['text'], func=lambda m: True)
@base(send_chat_action=False)
def get_all_messages(message: Message, current_user: User):
    if message.chat.type == 'private':
        text = 'Выберите действие в меню. 👇'

        return send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    pf = ProfanityFilter()

    answer_list = ['Фу! Как некультурно!', 'Мат - для лохов', 'Не матюкайся', 'Не матерись',
                   'Мне показалось, или ты быканул?', 'Мат - плохо', 'Не матерись дуралей',
                   'Не излагай свои мысли как прибей', 'Кто обзывается, тот сам так и называется']

    if pf.is_profane(message.text):
        send_message_private(message, random.choice(answer_list), reply_to_message_id=message.message_id)
