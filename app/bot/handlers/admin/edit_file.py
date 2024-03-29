from html import escape

from telebot.types import Message, CallbackQuery

from app.models import User
from app.services.files import edit_file, get_file, delete_file
from app.services.photos import get_photo, delete_photo
from ...base import base, callback_query_base
from ...helpers import send_message_private, save_delete_message, send_message_inline_private
from ...keyboards.default import get_menu_keyboard_markup, get_cancel_keyboard_markup
from ...keyboards.inline import get_edit_inline_markup, get_delete_photo_inline_markup
from ...loader import bot, bot_username


@bot.message_handler(regexp=f'^/file\\d+(@{bot_username})?$')
@base(is_admin=True)
def get_edit_file_handler(message: Message, current_user: User):
    id = message.text[5:].replace(f'@{bot_username}', '').strip()
    if not id.isnumeric():
        return send_message_private(message, 'Файл не найдено ❌')

    send_file_edit_menu(message, int(id), current_user.is_admin())


@bot.message_handler(commands=['start'], func=lambda m: m.text.startswith('/start file'))
@base()
def deep_link_edit_handler(message: Message, current_user: User):
    id = message.text[11:]
    if not id.isnumeric():
        return send_message_private(message, 'Файл не найдено ❌')

    send_file_edit_menu(message, int(id), current_user.is_admin())


@bot.message_handler(commands=['start'], func=lambda m: m.text.startswith('/start photo'))
@base()
def deep_link_edit_handler(message: Message, current_user: User):
    id = message.text[12:]

    if not id.isnumeric():
        return send_message_private(message, 'Фото не найдено ❌', reply_to_message_id=message.id)

    id = int(id)

    photo = get_photo(id)
    if not photo:
        return send_message_private(message, f'Фото с id <b>{id}</b> не найдено ❌', reply_to_message_id=message.id)

    markup = get_delete_photo_inline_markup('edit_photo', id) if current_user.is_admin() else None

    bot.send_photo(message.chat.id, photo.file_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_photo'))
@callback_query_base(is_admin=True)
def inline_edit_photo_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    query, option = call.data[10:].split('_')
    id = int(query)

    if option == 'cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return save_delete_message(chat_id, message_id)

    photo = get_photo(id)

    if not photo:
        bot.answer_callback_query(call.id, 'Фото уже удалено', show_alert=True)
        return save_delete_message(chat_id, message_id)
    elif option == 'delete':
        delete_photo(id)
        bot.answer_callback_query(call.id, 'Удаленно', show_alert=True)
        save_delete_message(chat_id, message_id)
    else:
        bot.answer_callback_query(call.id, 'Отменено')
        save_delete_message(chat_id, message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_file'))
@callback_query_base(is_admin=True)
def inline_edit_file_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    query, option = call.data[9:].split('_')
    id = int(query)

    if option == 'cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return save_delete_message(chat_id, message_id)

    file = get_file(id)
    if not file:
        bot.answer_callback_query(call.id, 'Файл уже удален', show_alert=True)
        return save_delete_message(chat_id, message_id)

    if option == 'edit':
        text = (f'Введите измененное название для файла:\n'
                f'<pre>{file.title}</pre>')

        markup = get_cancel_keyboard_markup()
        response = send_message_inline_private(call, text, reply_markup=markup)
        bot.register_next_step_handler(response, edit_file_handler, id=id)

        save_delete_message(chat_id, message_id)
    elif option == 'delete':
        delete_file(id)
        bot.answer_callback_query(call.id, 'Удаленно', show_alert=True)
        save_delete_message(chat_id, message_id)
    else:
        bot.answer_callback_query(call.id, 'Отменено')
        save_delete_message(chat_id, message_id)


@base(is_admin=True)
def edit_file_handler(message: Message, id: int, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Это {message.content_type}, а мне нужно задание для предмета!')
        return bot.register_next_step_handler(response, edit_file_handler, id=id, current_user=current_user)

    file = edit_file(id, escape(message.text))

    text = 'Файл изменен ✅'

    markup = get_menu_keyboard_markup(current_user.is_admin())
    send_message_private(message, text, reply_markup=markup)
    send_file_edit_menu(message, file.id, current_user.is_admin())


def send_file_edit_menu(message: Message, id: int, allow_editing: bool = True):
    file = get_file(id)

    if not file:
        return send_message_private(message, f'Файл с id <b>{id}</b> не найден ❌', reply_to_message_id=message.id)

    text = file.title

    markup = get_edit_inline_markup('edit_file', id) if allow_editing else None

    try:
        bot.send_document(message.chat.id, file.file_id, caption=text, reply_markup=markup)
    except Exception as e:
        if e.error_code == 400:
            return send_message_private(message, 'Похоже файл был удален ❌')
