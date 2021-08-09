from telebot.types import Message

from app.services.users import get_user, get_users
from ...base import base
from ...helpers import send_message_private
from ...loader import bot


@bot.message_handler(commands=['users_list'])
@base(is_admin=True)
def users_list_handler(message: Message):
    text = ''
    for user in get_users():
        text += f'{user.name}'

        if user.username:
            text += f' @{user.username}'

        text += f'\n/user_{user.id}\n\n'

    send_message_private(message, text.rstrip())


@bot.message_handler(regexp=f'^/user_\\d+(@{bot.get_me().username})?$')
@base(is_admin=True)
def get_user_handler(message: Message):
    id = int(message.text[6:].replace(f'@{bot.get_me().username}', '').strip())
    user = get_user(id)

    text = f'<a href="tg://user?id={user.id}">{user.name}</a>'

    if user.username:
        text += f' @{user.username}'

    text += f'\n\nСтатус: {user.status}\n' \
            f'\nДата первого обращения: \n<pre>{user.created_at}</pre>'

    photo_id = None
    try:
        photos = bot.get_user_profile_photos(id).photos

        if len(photos):
            photo_id = photos[0][-1].file_id
    except Exception as e:
        if e.error_code == 400:
            text += '<b>НЕ АКТИВНЫЙ❗</b>'

    if photo_id:
        return bot.send_photo(message.chat.id, photo_id, text)

    bot.send_message(message.chat.id, text)
