from app.bot.loader import bot


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Help')
