from telebot.types import Message, CallbackQuery

from ..loader import bot


def send_message_private(message: Message, text: str, *args, **kwargs):
    if message.chat.type == 'private':
        return bot.send_message(message.chat.id, text, *args, **kwargs)

    return bot.send_message(message.chat.id, mark_user(text, message.from_user.id), *args, **kwargs)


def send_message_inline_private(call: CallbackQuery, text: str, *args, **kwargs):
    if call.message.chat.type == 'private':
        return bot.send_message(call.message.chat.id, text, *args, **kwargs)

    return bot.send_message(call.message.chat.id, mark_user(text, call.from_user.id), *args, **kwargs)


def mark_user(text: str, user_id: int) -> str:
    text += f'<a href="tg://user?id={user_id}">⠀</a>'
    return text
