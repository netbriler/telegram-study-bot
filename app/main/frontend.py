from app.main import main
from flask import current_app
from flask_login import login_required


@main.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@main.route('/<path:path>')
@login_required
def index(path: str):
    return current_app.send_static_file('index.html')
