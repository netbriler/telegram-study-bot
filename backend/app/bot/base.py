import requests

from telebot.types import Message, CallbackQuery

from app.bot.loader import app, bot
from app.services.users import get_user, create_user, edit_user

from .keyboards.default import get_remove_keyboard_markup
from .utils import send_message_private


def base(is_admin=False):
    def error_boundary(func):

        def wrapper(message: Message, *args, **kwargs):
            try:
                bot.send_chat_action(message.chat.id, 'typing')

                if message.text == '❌Отменить❌':
                    return send_message_private(message, 'Ок 👍', reply_markup=get_remove_keyboard_markup())

                with app.app_context():
                    current_user = _get_or_create_user(message.from_user)
                    if is_admin and not current_user.is_admin():
                        return bot.reply_to(message, 'У вас нет прав')

                    func(message, current_user, *args, **kwargs)

                if message.content_type == 'text':
                    app.logger.debug(f'from_user: {message.from_user.id} message_id: {message.message_id} '
                                     f'text: {message.text}')

            except Exception as e:
                app.logger.error(e)

        return wrapper

    return error_boundary


def callback_query_base(is_admin=False):
    def error_boundary(func):

        def wrapper(call: CallbackQuery, *args, **kwargs):
            try:
                chat_id = call.message.chat.id
                message_id = call.message.message_id

                if call.data == 'cancel':
                    bot.answer_callback_query(call.id, 'Отменено')
                    return bot.delete_message(chat_id, message_id)

                with app.app_context():
                    current_user = _get_or_create_user(call.from_user)
                    if is_admin and not current_user.is_admin():
                        return bot.answer_callback_query(call.id, 'У вас нет прав')

                    func(call, current_user, *args, **kwargs)

                if call.data:
                    app.logger.debug(f'from_user: {call.from_user.id} chat_id: {chat_id} '
                                     f'message_id: {message_id} data: {call.data}')
            except Exception as e:
                app.logger.error(e)

        return wrapper

    return error_boundary


def _get_or_create_user(from_user):
    id = from_user.id
    user = get_user(id)

    name = from_user.first_name
    if from_user.last_name:
        name += ' ' + from_user.last_name

    username = from_user.username

    photo_id = None

    photos = bot.get_user_profile_photos(id).photos

    if len(photos) > 0:
        photo_id = photos[0][-1].file_id

        if not user or user.photo_id != photo_id:
            r = requests.get(bot.get_file_url(photo_id), allow_redirects=True)
            open(f'{app.config["APP_DIR"]}/static/pictures/{photo_id}.jpg', 'wb').write(r.content)

    if not user:
        user = create_user(id, name, username, photo_id)
    else:
        user = edit_user(id, name, username, photo_id)

    return user
