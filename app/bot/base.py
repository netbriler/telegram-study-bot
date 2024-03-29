import inspect

from telebot.types import Message, CallbackQuery, InlineQuery

from app.bot.loader import bot
from app.services.users import get_or_create_user, download_user_avatar
from app.utils.logging import logger
from .commands import set_super_admin_commands, set_admin_commands, delete_admin_commands
from .helpers import send_message_private, save_delete_message
from .keyboards.default import get_menu_keyboard_markup, get_remove_keyboard_markup


def base(is_admin: bool = False, is_super_admin: bool = False, send_chat_action: str = 'typing'):
    def decorator(func):
        @logger.catch
        def wrapper(message: Message, *args, **kwargs):
            if send_chat_action:
                bot.send_chat_action(message.chat.id, send_chat_action)

            from_user = message.from_user

            name = from_user.first_name
            if from_user.last_name:
                name += ' ' + from_user.last_name

            current_user = get_or_create_user(from_user.id, name, from_user.username)
            if current_user.is_banned():
                return bot.send_message(message.chat.id, 'Доступ ограничен ❌',
                                        reply_markup=get_remove_keyboard_markup())

            if message.content_type == 'text':
                logger.debug(f'from_user: {current_user} message_id: {message.message_id} '
                             f'text: {message.text}')

            if message.text == '❌ Отменить' or message.text == '/cancel':
                markup = get_menu_keyboard_markup(current_user.is_admin())
                return send_message_private(message, 'Ок 👍', reply_markup=markup)

            if is_super_admin and not current_user.is_super_admin():
                bot.reply_to(message, 'У вас нет прав')
            elif is_admin and not current_user.is_admin():
                bot.reply_to(message, 'У вас нет прав')
            else:
                kwargs['message'] = message
                kwargs['current_user'] = current_user

                _attributes_check(func, args, kwargs)

            download_user_avatar(current_user, bot)

            if current_user.is_super_admin():
                set_super_admin_commands(from_user.id, message.chat.id)
            elif current_user.is_admin():
                set_admin_commands(from_user.id, message.chat.id)
            else:
                delete_admin_commands(from_user.id, message.chat.id)

        return wrapper

    return decorator


def callback_query_base(is_admin: bool = False, is_super_admin: bool = False):
    def decorator(func):
        @logger.catch
        def wrapper(call: CallbackQuery, *args, **kwargs):
            chat_id = call.chat_instance if call.inline_message_id else call.message.chat.id
            message_id = call.inline_message_id if call.inline_message_id else call.message.message_id

            if not call.inline_message_id and call.data == 'cancel':
                bot.answer_callback_query(call.id, 'Отменено')
                return save_delete_message(chat_id, message_id)

            from_user = call.from_user

            name = from_user.first_name
            if from_user.last_name:
                name += ' ' + from_user.last_name

            current_user = get_or_create_user(from_user.id, name, from_user.username)
            if current_user.is_banned():
                return bot.answer_callback_query(call.id, 'Доступ ограничен ❌', show_alert=True)

            if call.data:
                logger.debug(f'from_user: {current_user} chat_id: {chat_id} '
                             f'message_id: {message_id} data: {call.data}')

            if is_super_admin and not current_user.is_super_admin():
                return bot.answer_callback_query(call.id, 'У вас нет прав', show_alert=True)
            elif is_admin and not current_user.is_admin():
                return bot.answer_callback_query(call.id, 'У вас нет прав', show_alert=True)
            else:
                kwargs['call'] = call
                kwargs['current_user'] = current_user

                _attributes_check(func, args, kwargs)

            download_user_avatar(current_user, bot)

            if not call.inline_message_id:
                if current_user.is_super_admin():
                    set_super_admin_commands(from_user.id, chat_id)
                elif current_user.is_admin():
                    set_admin_commands(from_user.id, chat_id)
                else:
                    delete_admin_commands(from_user.id, chat_id)

        return wrapper

    return decorator


def inline_base():
    def decorator(func):
        @logger.catch
        def wrapper(inline_query: InlineQuery, *args, **kwargs):
            from_user = inline_query.from_user

            name = from_user.first_name
            if from_user.last_name:
                name += ' ' + from_user.last_name

            current_user = get_or_create_user(from_user.id, name, from_user.username)
            if current_user.is_banned():
                return

            logger.debug(f'from_user: {current_user} chat_type: {inline_query.chat_type} data: {inline_query.query}')

            kwargs['inline_query'] = inline_query
            kwargs['current_user'] = current_user

            _attributes_check(func, args, kwargs)

            download_user_avatar(current_user, bot)

        return wrapper

    return decorator


def _attributes_check(func, args, kwargs: dict):
    func_args_list = inspect.getfullargspec(func).args

    kwargs = {k: v for k, v in kwargs.items() if k in func_args_list}

    return func(*args, **kwargs)
