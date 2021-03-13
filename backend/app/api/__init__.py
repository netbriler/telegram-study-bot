from flask import abort, Blueprint, json, jsonify
from flask.wrappers import Response

from flask_login import current_user

api = Blueprint('api', __name__)


@api.route('/<path:path>')
def catch_all(path: str):
    abort(404, 'Not Found')


@api.errorhandler(Exception)
def handle_exception(e: Exception):
    return jsonify({
        'ok': False,
        'code': e.code,
        'description': e.description
    }), e.code


@api.after_request
def after_request(response: Response):
    response_data = json.loads(response.get_data())

    if 'ok' not in response_data or response_data['ok']:
        data = dict()
        data['ok'] = True
        data['response'] = json.loads(response.get_data())
        response.set_data(json.dumps(data, sort_keys=False))
    return response


@api.before_request
def before_request():
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(401)


from . import subjects
from . import timetable
from . import tasks
from . import users
