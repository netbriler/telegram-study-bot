import telebot
from flask import jsonify, current_app, request
from flask import url_for
from flask_login import login_required

from app.bot import bot
from app.main import main


@main.route('/setWebhook')
@login_required
def set_webhook():
    bot.set_webhook(url_for('main.webhook', _external=True, _scheme='https'))
    return 'ok', 200


@main.route('/getWebhookInfo')
@login_required
def get_webhook_info():
    return jsonify(bot.get_webhook_info().__dict__)


@main.route('/deleteWebhook')
@login_required
def delete_webhook():
    bot.delete_webhook()
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
