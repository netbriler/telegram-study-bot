from telebot.types import Message

from ...loader import bot
from ...base import base
from ...keyboards.default import get_menu_keyboard_markup
from ...utils import send_message_private

from app.models import User


@bot.message_handler(commands=['start'])
@base()
def start_handler(message: Message, current_user: User):
    text = (f'Привет {current_user.name}!\n'
            'Я учебный бот и я могу сообщать тебе дз, расписание и всю информацию по предмету.\n'
            'Выберите действие в меню. 👇')

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

