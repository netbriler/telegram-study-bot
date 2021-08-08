import telebot
from flask import current_app

bot = telebot.TeleBot(current_app.config['TELEGRAM_BOT_TOKEN'], parse_mode='HTML', threaded=False)
