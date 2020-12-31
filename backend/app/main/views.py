"""This is the views page, which is similar to what the routes do for the API.
The difference is rather than routes, this renders and displays HTML pages"""

from app.main import main
from flask import (
    render_template,
    redirect,
    url_for,
    abort,
    flash,
    request,
    current_app,
    make_response,
    jsonify
)
from flask_login import login_user, logout_user, login_required, current_user, login_manager

from app import db

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
        return redirect('/')

    abort(400)


@main.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(id=485682772).first()
    login_user(user, remember=True)

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@main.route('/<path:path>')
@login_required
def index(path):
    return current_app.send_static_file('index.html')
