from app.main import main
from flask import redirect, abort, request, current_app, jsonify, url_for
from flask_login import login_required

import telebot
from app.bot import bot


@main.route('/setWebhook')
@login_required
def set_webhook():
    bot.set_webhook(url_for('main.webhook', _external=True, _scheme='https'))
    return 'ok', 200


@main.route('/' + current_app.config['TELEGRAM_BOT_TOKEN'], methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return 'ok', 200
