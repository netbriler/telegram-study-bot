from flask import redirect, abort, request, current_app, jsonify, render_template, url_for, Response
from flask_login import login_user, logout_user, login_required, current_user

from app.bot.loader import bot
from app.main import main
from app.models import User
from app.services.telegram_auth import verify_authorization, safe_parse_webapp_init_data
from app.services.users import get_user, count_users, create_user, edit_user_status
from app.utils.logging import logger


@main.route('/login_redirect', methods=['GET'])
def login_redirect():
    data = request.args.to_dict()

    if 'hash' not in data:
        abort(400)

    if verify_authorization(data, current_app.config['TELEGRAM_BOT_TOKEN']):
        if not count_users():
            create_user(data['id'], data['first_name'], data['username'])
            edit_user_status(data['id'], 'super_admin')

        user = get_user(id=data['id'])
        if not user:
            abort(400, 'This account is not present in the database')
        if not user.is_admin():
            abort(403, 'Admin panel is available only for administrators, contact the creator to get the rights')
        login_user(user, remember=True)

        logger.info(f'{user} logged')

        return redirect('/')

    abort(400)


@main.route('/login_web_app', methods=['GET', 'POST'])
def login_web_app():
    if current_user.is_authenticated:
        return redirect(url_for('main.index', _external=True))

    if not request.form or '_auth' not in request.form.to_dict():
        content = """

            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title></title>
            <script src="https://telegram.org/js/telegram-web-app.js?1"></script>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"
             integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ=="
              crossorigin="anonymous" referrerpolicy="no-referrer"></script>

            <script>
                Telegram.WebApp.ready();

                $.ajax({
                    type: 'POST',
                    url: '/login_web_app',
                    data: {_auth: Telegram.WebApp.initData},
                    success: function(response){
                        document.body.innerText = 'Вы успешно авторизовались, перезапустите страницу';
                        window.location.href = response
                    },
                    error: function() {
                        document.body.innerText = 'У вас нет прав';
                    },
                });

            </script>
        </head>
        <body>
        </body>
        </html>

            """

        return Response(content, mimetype='text/html')

    data = request.form.to_dict()

    data = safe_parse_webapp_init_data(bot.token, data['_auth'])
    if data:
        data = data['user']
        if not count_users():
            create_user(data['id'], data['first_name'], data['username'])
            edit_user_status(data['id'], 'super_admin')

        user = get_user(id=data['id'])
        if not user:
            abort(400, 'This account is not present in the database')
        if not user.is_admin():
            abort(403, 'Admin panel is available only for administrators, contact the creator to get the rights')
        login_user(user, remember=True)

        logger.info(f'{user} logged')

        return url_for('main.index', _external=True), 200
    else:
        abort(403, 'Fake user')


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
