from telebot.types import Message
from app.bot.loader import bot


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Howdy, how are you doing?')
