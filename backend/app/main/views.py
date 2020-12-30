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
    make_response)
from app import db

from app.models.tasks import Task
from app.models.subjects import Subject


@main.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@main.route('/<path:path>')
def index(path):
    return current_app.send_static_file('index.html')
