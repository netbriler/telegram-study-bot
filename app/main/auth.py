from flask import redirect, abort, request, current_app, jsonify, render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.logging import logger

from app.bot.loader import bot
from app.main import main
from app.models import User
from app.services.telegram_auth import verify_authorization


@main.route('/login_redirect', methods=['GET'])
def login_redirect():
    data = request.args.to_dict()

    if 'hash' not in data:
        abort(400)

    if verify_authorization(data, current_app.config['TELEGRAM_BOT_TOKEN']):
        user = User.query.filter_by(id=data['id']).first()
        if not user:
            abort(400, 'This account is not present in the database')
        if not user.is_admin():
            abort(403, 'Admin panel is available only for administrators, contact the creator to get the rights')
        login_user(user, remember=True)

        logger.info(f'{user} logged')

        return redirect('/')

    abort(400)


@main.route('/login', methods=['GET', 'POST'])
def login():
    bot_username = bot.get_me().username

    return render_template('login.html', bot_username=bot_username)


@main.route('/login/<string:user_id>', methods=['GET', 'POST'])
def _login_user(user_id):
    if current_app.config['DEBUG']:
        user = User.query.filter_by(id=user_id).first()
        login_user(user, remember=True)
        logger.info(f'{user} logged')

        return jsonify(current_user.to_json())
    return redirect(url_for('main.login'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
