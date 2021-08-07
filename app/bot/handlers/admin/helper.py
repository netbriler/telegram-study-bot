from app.models import User
from telebot.types import Message

from ...base import base, get_or_create_user
from ...keyboards.default import get_cancel_keyboard_markup
from ...loader import bot
from ...utils import send_message_private


@bot.message_handler(commands=['get_id'])
@base(is_admin=True)
def get_id_handler(message: Message, current_user: User):
    bot.delete_message(message.chat.id, message.message_id)

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
def file_add_handler(message: Message, current_user: User):
    text = 'Отправьте мне файл, а я пришлю его id'

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, file_handler)


@base(is_admin=True)
def file_handler(message: Message, current_user: User):
    if message.content_type == 'document':
        bot.reply_to(message, f'<pre>{message.document.file_id}</pre>')
    else:
        response = bot.reply_to(message, f'Мне нужен документ, а вы отправили {message.content_type}',
                                reply_markup=get_cancel_keyboard_markup())
        bot.register_next_step_handler(response, file_handler)


@bot.message_handler(commands=['call_all'])
@base(is_admin=True)
def call_all_members_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    text = 'Внимание, внимание!'

    bot.delete_message(chat_id, message.message_id)

    if message.chat.type != 'private':
        chat_members = bot.get_chat_administrators(chat_id)
        for chat_member in chat_members:
            text += f'<a href="tg://user?id={chat_member.user.id}">⠀</a>'

        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, 'Ну и кого в личке позвать то?)')


@bot.message_handler(commands=['delete'])
@base(is_admin=True)
def delete_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    if not message.reply_to_message or not message.reply_to_message.from_user.is_bot:
        return bot.reply_to(message, 'Ответьте на мое сообщение командой чтобы удалить')

    bot.delete_message(chat_id, message.reply_to_message.message_id)
    bot.delete_message(chat_id, message.message_id)


@bot.message_handler(commands=['load_all'])
@base(is_super_admin=True)
def call_all_members_handler(message: Message, current_user: User):
    chat_id = message.chat.id
    text = 'Готово'

    bot.delete_message(chat_id, message.message_id)

    if message.chat.type != 'private':
        chat_members = bot.get_chat_administrators(chat_id)
        for chat_member in chat_members:
            if not chat_member.user.is_bot:
                user = get_or_create_user(chat_member.user)
                text += f'\n<a href="tg://user?id={user.id}">{user.name}</a>'

        bot.send_message(current_user.id, text)
    else:
        bot.send_message(current_user.id, 'Ну и кого в личке добавлять то?)')
