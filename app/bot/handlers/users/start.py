from telebot.apihelper import _make_request
from telebot.types import Message
from flask import url_for
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

    if current_user.is_admin():
        params = {
            'chat_id': message.chat.id,
            'menu_button': '{"type": "web_app",\
                            "web_app": {"url": "'+url_for('main.login_web_app', _external=True)+'"},\
                            "text": "Admin menu"}'
        }

        _make_request(bot.token, 'setChatMenuButton', params=params, method='post')

    send_message_private(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
