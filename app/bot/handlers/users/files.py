from telebot.types import CallbackQuery
from telebot.types import InlineQuery, InlineQueryResultCachedDocument, InlineQueryResultArticle, \
    InputTextMessageContent

from app.models import User
from app.services.files import get_file
from app.utils.helper import generate_inline_id
from ...base import callback_query_base, inline_base
from ...helpers import mark_user
from ...keyboards.inline import get_edit_inline_markup
from ...loader import bot, bot_username


@bot.inline_handler(lambda q: q.query.startswith('file'))
@inline_base()
def inline_file(inline_query: InlineQuery):
    id = inline_query.query[4:]

    results = [InlineQueryResultArticle(
        id=generate_inline_id('not_found'),
        title='Файл не найден',
        thumb_url='https://images.emojiterra.com/google/android-11/512px/274c.png',
        input_message_content=InputTextMessageContent('Файл не найден ❌')
    )]

    if not id or not id.isdigit():
        return bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

    file = get_file(int(id))

    if not file:
        return bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

    file_available = True

    try:
        bot.get_file(file.file_id)
    except Exception as e:
        file_available = e.result_json['description'] == 'Bad Request: file is too big'

    if file_available:
        results = [InlineQueryResultCachedDocument(
            id=generate_inline_id(file.id),
            title=file.title,
            caption=file.title,
            document_file_id=file.file_id
        )]
    else:
        results = [InlineQueryResultArticle(
            id=generate_inline_id('error'),
            title=file.title,
            description='Похоже файл был удален',
            thumb_url='https://images.emojiterra.com/google/android-11/512px/274c.png',
            input_message_content=InputTextMessageContent(f'Файл "<i>{file.title.lower()}</i>" не найден ❌',
                                                          parse_mode='HTML')
        )]

    bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('file'))
@callback_query_base()
def inline_file_handler(call: CallbackQuery, current_user: User):
    deep_link = f'tg://resolve?domain={bot_username}&start=file'

    file_id = int(call.data[5:])

    file = get_file(file_id)
    if not file:
        return bot.answer_callback_query(call.id, 'Файл не найден')

    text = f'{file.title}<a href="{deep_link}{file.id}">⠀</a>'

    if call.message.chat.type != 'private':
        text = mark_user(text, call.from_user.id)

    markup = get_edit_inline_markup('edit_file', file.id) if current_user.is_admin() else None

    try:
        bot.send_document(call.message.chat.id, file.file_id, caption=text, reply_markup=markup)
        return bot.answer_callback_query(call.id, file.title)
    except Exception as e:
        if e.error_code == 400:
            return bot.answer_callback_query(call.id, 'Похоже файл был удален')
