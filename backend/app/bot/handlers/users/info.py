from telebot.types import Message, CallbackQuery

from ...loader import bot
from ...base import base, callback_query_base
from ...keyboards.inline import get_subjects_inline_markup, get_subject_files_inline_markup
from ...utils import send_message_private

from app.models import User

from app.services.subjects import get_subject
from app.services.files import get_file


@bot.message_handler(regexp='^👀Информация👀$')
@bot.message_handler(commands=['info'])
@base()
def start_info(message: Message, current_user: User):
    text = 'Узнать информацию по предмету: '

    send_message_private(message, text, reply_markup=get_subjects_inline_markup('info'))


@bot.callback_query_handler(func=lambda call: call.data.startswith('info'))
@callback_query_base()
def inline_info_handler(call: CallbackQuery, current_user: User):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'info_cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return bot.delete_message(chat_id, message_id)

    data = call.data.split('_')
    subject = get_subject(data[1])

    text = (f'<b>{subject.name}</b>\n\n'
            f'Аудитория: <b>{subject.audience}</b>\n'
            f'Учитель: <b>{subject.teacher}</b>\n\n'
            f'{subject.info}').rstrip()

    if subject.files:
        text += '\nСписок документов 👇'

    if call.message.chat.type != 'private':
        text += f'<a href="tg://user?id={call.from_user.id}">⠀</a>'

    bot.send_message(chat_id, text, reply_markup=get_subject_files_inline_markup(subject), disable_web_page_preview=True)
    return bot.answer_callback_query(call.id, subject.name)


@bot.callback_query_handler(func=lambda call: call.data.startswith('file'))
@callback_query_base()
def inline_file_handler(call: CallbackQuery, current_user: User):
    data = call.data.split('_')
    file = get_file(data[1])
    if not file:
        return bot.answer_callback_query(call.id, 'Файл не найден')

    text = file.title

    if call.message.chat.type != 'private':
        text = f'{text}<a href="tg://user?id={call.from_user.id}">⠀</a>'

    try:
        bot.send_document(call.message.chat.id, file.file_id, caption=text)
    except Exception as e:
        if e.error_code == 400:
            return bot.answer_callback_query(call.id, 'Похоже файл был удален')
