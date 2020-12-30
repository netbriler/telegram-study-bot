from flask import abort, Blueprint, json, jsonify

api = Blueprint('api', __name__)


@api.route('/<path:path>')
def catch_all(path):
    abort(404, 'Not Found')


@api.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        'ok': False,
        'code': e.code,
        'description': e.description
    })


@api.after_request
def after_request(response):
    response_data = json.loads(response.get_data())

    if 'ok' not in response_data or response_data['ok']:
        data = dict()
        data['ok'] = True
        data['response'] = json.loads(response.get_data())
        response.set_data(json.dumps(data, sort_keys=False))
    return response


from . import subjects
