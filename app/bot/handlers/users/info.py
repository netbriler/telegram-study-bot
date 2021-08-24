from telebot.types import Message, CallbackQuery

from app.services.files import get_file
from app.services.subjects import get_subject
from ...base import base, callback_query_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_subjects_inline_markup, get_subject_files_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^📚 Информация$')
@bot.message_handler(commands=['info'])
@base()
def start_info(message: Message):
    text = 'Узнать информацию по предмету: '

    send_message_private(message, text, reply_markup=get_subjects_inline_markup('info'))


@bot.callback_query_handler(func=lambda call: call.data.startswith('info'))
@callback_query_base()
def inline_info_handler(call: CallbackQuery):
    chat_id = call.message.chat.id

    if call.data == 'info_cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return bot.delete_message(chat_id, call.message.message_id)

    subject_codename = call.data.split('_')[1]
    subject = get_subject(subject_codename)

    text = (f'<b>{subject.name}</b>\n\n'
            f'Аудитория: <b>{subject.audience}</b>\n'
            f'Учитель: <b>{subject.teacher}</b>\n\n'
            f'{subject.info}').rstrip()

    if subject.files:
        text += '\nСписок документов 👇'

    if call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_subject_files_inline_markup(subject)
    bot.send_message(chat_id, text, reply_markup=markup, disable_web_page_preview=True)

    return bot.answer_callback_query(call.id, subject.name)


@bot.callback_query_handler(func=lambda call: call.data.startswith('file'))
@callback_query_base()
def inline_file_handler(call: CallbackQuery):
    file_id = int(call.data.split('_')[1])

    file = get_file(file_id)
    if not file:
        return bot.answer_callback_query(call.id, 'Файл не найден')

    text = file.title

    if call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    try:
        bot.send_document(call.message.chat.id, file.file_id, caption=text)
        return bot.answer_callback_query(call.id, file.title)
    except Exception as e:
        if e.error_code == 400:
            return bot.answer_callback_query(call.id, 'Похоже файл был удален')
