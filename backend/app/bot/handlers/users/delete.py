from telebot.types import Message

from ...loader import bot
from ...base import base

from app.models import User


@bot.message_handler(commands=['delete'])
@base()
def delete_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    if not message.reply_to_message or not message.reply_to_message.from_user.is_bot:
        return bot.reply_to(message, 'Ответьте на мое сообщение командой чтобы удалить')

    bot.delete_message(chat_id, message.reply_to_message.message_id)
    bot.delete_message(chat_id, message.message_id)


