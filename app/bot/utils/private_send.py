from telebot.types import Message, CallbackQuery

from ..loader import bot


def send_message_private(message: Message, text, *args, **kwargs):
    if message.chat.type == 'private':
        return bot.send_message(message.chat.id, text, *args, **kwargs)
    else:
        text += f'<a href="tg://user?id={message.from_user.id}">⠀</a>'
        return bot.send_message(message.chat.id, text, *args, **kwargs)


def send_message_inline_private(call: CallbackQuery, text, *args, **kwargs):
    if call.message.chat.type == 'private':
        return bot.send_message(call.message.chat.id, text, *args, **kwargs)
    else:
        text += f'<a href="tg://user?id={call.from_user.id}">⠀</a>'
        return bot.send_message(call.message.chat.id, text, *args, **kwargs)
