from telebot.types import Message
from app.bot.loader import bot

from app.bot.base import base

from app.models import User


@bot.message_handler(commands=['start'])
@base()
def send_welcome(message: Message, current_user: User):
    message = (f'Привет {current_user.name}!\n'
               'Я учебный бот и я могу сообщать тебе дз, расписание и всю информацию по предмету.\n'
               'Выбери действие в меню. 👇')

    bot.send_message(current_user.id, message)

