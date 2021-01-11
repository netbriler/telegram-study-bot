import telebot
from flask import current_app

from app import create_app

bot = telebot.TeleBot(current_app.config['TELEGRAM_BOT_TOKEN'], parse_mode='HTML')

app = create_app(current_app.config['CONFIG_KEY'])
