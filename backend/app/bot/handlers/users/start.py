from app.bot.loader import bot


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Howdy, how are you doing?')
