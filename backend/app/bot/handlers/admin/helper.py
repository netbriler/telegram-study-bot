from telebot.types import Message

from ...loader import bot
from ...base import base

from app.models import User


@bot.message_handler(commands=['get_id'])
@base(is_admin=True)
def get_id_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return bot.reply_to(message, 'Ответьте на сообщение командой чтобы узнать id')

    bot.delete_message(chat_id, message.message_id)

    bot.send_message(current_user.id, f'message_id: {message.reply_to_message.message_id}\n'
                                      f'chat_id: {message.reply_to_message.chat.id}')


@bot.message_handler(commands=['call_all'])
@base(is_admin=True)
def call_all_members_handler(message: Message, current_user: User):
    text = 'Внимание, внимание!'

    if message.chat.type != 'private':
        chat_members = bot.get_chat_administrators(message.chat.id)
        for chat_member in chat_members:
            text += f'<a href="tg://user?id={chat_member.user.id}">́</a>'

        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Ну и кого в личке похвать то?)')


@bot.message_handler(commands=['delete'])
@base(is_admin=True)
def delete_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    if not message.reply_to_message or not message.reply_to_message.from_user.is_bot:
        return bot.reply_to(message, 'Ответьте на мое сообщение командой чтобы удалить')

    bot.delete_message(chat_id, message.reply_to_message.message_id)
    bot.delete_message(chat_id, message.message_id)
