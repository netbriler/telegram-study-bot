from flask import current_app, Response
from flask_login import login_required

from app.main import main


@main.route('/logs')
@login_required
def logs():
    with open(current_app.config['LOGGING_DIR'] + '/log.out', 'r', encoding='utf-8') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')


@main.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@main.route('/<path:path>')
@login_required
def index(path: str):
    return current_app.send_static_file('index.html')
