from telebot.types import Message, CallbackQuery

from ...loader import bot
from ...base import base, callback_query_base

from app.models import User


@bot.message_handler(content_types=['text'], func=lambda m: True)
@base()
def get_all_messages(message: Message, current_user: User):
    pass


@bot.callback_query_handler(func=lambda call: True)
@callback_query_base()
def get_all_callback_queries(call: CallbackQuery, current_user: User):
    pass
