from telebot.types import Message
from app.bot.loader import bot

from app.bot.base import base
from app.bot.keyboards.default import get_menu_keyboard_markup, get_remove_keyboard_markup

from app.models import User


@bot.message_handler(commands=['keyboard'])
@base()
def send_welcome(message: Message, current_user: User):
    text = 'Выбери действие в меню. 👇'

    if message.chat.type == 'private':
        bot.send_message(message.chat.id, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
    else:
        bot.reply_to(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))


@bot.message_handler(commands=['keyboard_off'])
@base()
def send_welcome(message: Message, current_user: User):
    text = 'Меню отключено. ❌'

    if message.chat.type == 'private':
        bot.send_message(message.chat.id, text, reply_markup=get_remove_keyboard_markup())
    else:
        bot.reply_to(message, text, reply_markup=get_remove_keyboard_markup())

