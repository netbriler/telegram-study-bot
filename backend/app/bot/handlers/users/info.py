from telebot.types import Message, CallbackQuery

from ...loader import bot
from ...base import base, callback_query_base
from ...keyboards.inline import get_subjects_inline_markup
from ...utils import send_message_private

from app.models import User

from app.services.subjects import get_subject


@bot.message_handler(regexp='^👀Информация👀$')
@bot.message_handler(commands=['info'])
@base()
def start_info(message: Message, current_user: User):
    text = 'Узнать информацию по предмету: '

    bot.send_message(message.chat.id, text, reply_markup=get_subjects_inline_markup('info'))


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

    text = (f'{subject.name}\n'
            f'Учитель: <b>{subject.teacher}</b>\n'
            f'{subject.info}')

    if call.message.chat.type != 'private':
        text = f'<a href="tg://user?id={call.from_user.id}">*</a>{text}'

    bot.send_message(chat_id, text, disable_web_page_preview=True)

