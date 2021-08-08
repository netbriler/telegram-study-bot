from telebot.types import Message

from app.models import User
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_menu_keyboard_markup
from ...loader import bot


@bot.message_handler(commands=['start'])
@base()
def start_handler(message: Message, current_user: User):
    text = (f'Привет {current_user.name}!\n'
            'Нажми /help чтобы узнать чем я могу тебе помочь')

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
