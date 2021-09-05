from telebot.types import InlineQueryResultArticle, InlineQuery, InputTextMessageContent, \
    InlineQueryResultCachedDocument
from telebot.types import Message, CallbackQuery

from app.services.subjects import get_subject, recognize_subject, Subject
from app.utils.helper import generate_inline_id
from ...base import base, callback_query_base, inline_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_subjects_inline_markup, get_subject_files_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^📚 Информация$')
@bot.message_handler(commands=['info'])
@base()
def start_info(message: Message):
    text = 'Узнать информацию по предмету: '

    send_message_private(message, text, reply_markup=get_subjects_inline_markup('info'))


@bot.inline_handler(lambda q: q.query.strip())
@inline_base()
def inline_info(inline_query: InlineQuery):
    subject = recognize_subject(inline_query.query)

    text = _get_text(subject)

    results = [InlineQueryResultArticle(
        id=generate_inline_id(subject.codename),
        title=subject.name,
        description=f'Аудитория: {subject.audience}\nУчитель: {subject.teacher}',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/1f4da.png',
        input_message_content=InputTextMessageContent(text, parse_mode='HTML', disable_web_page_preview=True),
        reply_markup=get_subject_files_inline_markup(subject, inline=True)
    )]

    for file in subject.files:
        try:
            bot.get_file(file.file_id)
        except Exception as e:
            if e.result_json['description'] != 'Bad Request: file is too big':
                continue

        results.append(InlineQueryResultCachedDocument(
            id=generate_inline_id(file.id),
            title=file.title,
            caption=file.title,
            document_file_id=file.file_id
        ))

    bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('info'))
@callback_query_base()
def inline_info_handler(call: CallbackQuery):
    chat_id = call.message.chat.id

    if call.data == 'info_cancel':
        bot.answer_callback_query(call.id, 'Отменено')
        return bot.delete_message(chat_id, call.message.message_id)

    subject_codename = call.data[5:]
    subject = get_subject(subject_codename)

    if not subject:
        bot.answer_callback_query(call.id, 'Предмет не найден')
        return bot.edit_message_reply_markup(chat_id, call.message.message_id,
                                             reply_markup=get_subjects_inline_markup('info'))

    text = _get_text(subject)

    if call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_subject_files_inline_markup(subject)
    bot.send_message(chat_id, text, reply_markup=markup, disable_web_page_preview=True)

    return bot.answer_callback_query(call.id, subject.name)


def _get_text(subject: Subject):
    text = (f'<b>{subject.name}</b>\n\n'
            f'Аудитория: <b>{subject.audience}</b>\n'
            f'Учитель: <b>{subject.teacher}</b>\n\n'
            f'{subject.info}').rstrip()

    if subject.files:
        text += '\n\nСписок документов 👇'

    return text
