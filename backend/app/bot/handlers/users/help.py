from telebot.types import Message
from app.bot.loader import bot


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    bot.reply_to(message, 'Help')
