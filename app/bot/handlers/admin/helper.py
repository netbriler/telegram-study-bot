from telebot.types import Message

from app.models import User
from ...base import base, get_or_create_user
from ...helpers import send_message_private, mark_user, save_delete_message
from ...keyboards.default import get_cancel_keyboard_markup
from ...loader import bot


@bot.message_handler(commands=['get_id'])
@base(is_admin=True, send_chat_action=None)
def get_id_handler(message: Message, current_user: User):
    save_delete_message(message.chat.id, message.message_id)

    if not message.reply_to_message:
        return bot.send_message(current_user.id, 'Ответьте на сообщение командой чтобы узнать его id')

    message_id = message.reply_to_message.message_id
    chat_id = message.reply_to_message.chat.id

    forwarded_message = bot.forward_message(current_user.id, chat_id, message_id)

    text = (f'message_id: {message_id}\n'
            f'chat_id: {chat_id}\n'
            f'from_user: {message.reply_to_message.from_user.id}')

    bot.send_message(current_user.id, text, reply_to_message_id=forwarded_message.message_id)


@bot.message_handler(commands=['get_file_id'])
@base(is_admin=True)
def file_add_handler(message: Message):
    text = 'Отправьте мне файл, а я пришлю его id'

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, file_handler)


@base(is_admin=True)
def file_handler(message: Message):
    if message.content_type == 'document':
        bot.reply_to(message, f'<pre>{message.document.file_id}</pre>')
        file_add_handler(message)
    else:
        response = bot.reply_to(message, f'Мне нужен документ, а вы отправили {message.content_type}',
                                reply_markup=get_cancel_keyboard_markup())
        bot.register_next_step_handler(response, file_handler)


@bot.message_handler(commands=['call_all'])
@base(is_admin=True)
def call_all_members_handler(message: Message):
    chat_id = message.chat.id
    text = 'Внимание, внимание!'

    save_delete_message(chat_id, message.message_id)

    if message.chat.type != 'private':
        chat_members = bot.get_chat_administrators(chat_id)
        for chat_member in chat_members:
            text = mark_user(text, chat_member.user.id)

        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, 'Ну и кого в личке позвать то?)')


@bot.message_handler(commands=['delete'])
@base(is_admin=True, send_chat_action=None)
def delete_handler(message: Message):
    chat_id = message.chat.id
    if not message.reply_to_message or not message.reply_to_message.from_user.is_bot:
        save_delete_message(chat_id, message.message_id)
        return bot.send_message(message.from_user.id, 'Ответьте /delete на мое сообщение чтобы удалить')

    save_delete_message(chat_id, message.message_id)
    save_delete_message(chat_id, message.reply_to_message.message_id)


@bot.message_handler(commands=['load_all'])
@base(is_super_admin=True, send_chat_action=None)
def call_all_members_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    text = 'Готово'

    save_delete_message(chat_id, message.message_id)

    if message.chat.type != 'private':
        chat_members = bot.get_chat_administrators(chat_id)
        for chat_member in chat_members:
            if not chat_member.user.is_bot:
                name = chat_member.user.first_name
                if chat_member.user.last_name:
                    name += ' ' + chat_member.user.last_name

                user = get_or_create_user(chat_member.user.id, name, chat_member.user.username)
                text += f'\n<a href="tg://user?id={user.id}">{user.name}</a>'

        bot.send_message(current_user.id, text)
    else:
        bot.send_message(current_user.id, 'Ну и кого в личке добавлять то?)')
