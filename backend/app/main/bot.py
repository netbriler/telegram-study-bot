import urllib

from app.main import main
from flask import request, abort, current_app, url_for, send_file, jsonify
from flask_login import login_required

import telebot
from app.bot import bot


@main.route('/setWebhook')
@login_required
def set_webhook():
    bot.set_webhook(url_for('main.webhook', _external=True, _scheme='https'))
    return 'ok', 200


@main.route('/file/<string:file_id>')
@login_required
def get_file(file_id: str):
    try:
        return jsonify(bot.get_file(file_id).__dict__)
    except:
        return 'Bad Request: invalid file_id ', 400


@main.route('/' + current_app.config['TELEGRAM_BOT_TOKEN'], methods=['POST'])
def webhook():
    try:
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    except:
        pass
    return 'ok', 200
