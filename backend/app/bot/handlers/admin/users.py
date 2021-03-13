from app.models import User
from app.services.users import get_user, get_users
from telebot.types import Message

from ...base import base
from ...loader import bot
from ...utils import send_message_private


@bot.message_handler(commands=['users_list'])
@base(is_admin=True)
def users_list_handler(message: Message, current_user: User):
    text = ''
    for user in get_users():
        print(user.to_json())
        text += f'{user.name}'

        if user.username:
            text += f' @{user.username}'

        text += f'\n/user_{user.id}\n\n'

    send_message_private(message, text.rstrip())


@bot.message_handler(regexp=f'^/user_\\d+(@{bot.get_me().username})?$')
@base(is_admin=True)
def get_user_handler(message: Message, current_user: User):
    id = int(message.text[6:].replace(f'@{bot.get_me().username}', '').strip())
    user = get_user(id)

    text = f'<a href="tg://user?id={user.id}">{user.name}</a>'

    if user.username:
        text += f' @{user.username}'

    text += f'\n\nСтатус: {user.status}\n'
    text += f'\nДата первого обращения: \n<pre>{user.created_at}</pre>'

    if user.photo_id:
        bot.send_photo(message.chat.id, user.photo_id, text)
    else:
        print(text)
        bot.send_message(message.chat.id, text)
