from telebot.types import Message
from app.bot.loader import bot

from app.bot.base import base
from app.bot.keyboards.default import get_menu_keyboard_markup

from app.models import User


@bot.message_handler(commands=['start'])
@base()
def send_welcome(message: Message, current_user: User):
    text = (f'Привет {current_user.name}!\n'
            'Я учебный бот и я могу сообщать тебе дз, расписание и всю информацию по предмету.\n'
            'Выбери действие в меню. 👇')

    if message.chat.type == 'private':
        bot.send_message(message.chat.id, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
    else:
        bot.reply_to(message, text, reply_markup=get_menu_keyboard_markup(current_user.is_admin()))
