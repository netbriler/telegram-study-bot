import telebot
from app import create_app
from flask import current_app

bot = telebot.TeleBot(current_app.config['TELEGRAM_BOT_TOKEN'], parse_mode='HTML', threaded=False)

app = create_app(current_app.config['CONFIG_KEY'])
