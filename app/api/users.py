from flask import jsonify, current_app, abort, request
from flask_login import current_user

from app.api import api
from app.exceptions import BadRequest
from app.models.users import get_user_status_title
from app.services.users import get_user, get_users, edit_user_status


@api.route('/users', methods=['GET'])
def _get_users():
    try:
        users = get_users()
        return jsonify(list(map(lambda s: s.to_json(), users)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/users/<int:id>', methods=['GET'])
def _get_user(id: int):
    try:
        user = get_user(id)
        if not user:
            raise BadRequest('user not found')

        return jsonify(user.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/users/<int:id>', methods=['PATCH'])
def _update_user_status(id: int):
    try:
        assert request.json
        assert request.json['status']
        status = request.json['status']

        user = get_user(id)
        if not user:
            raise BadRequest('user not found')

        statuses_to_edit = current_user.get_statuses_to_edit()
        if status not in statuses_to_edit:
            raise BadRequest('support only this statuses: ' + ','.join(statuses_to_edit))

        if user.status not in statuses_to_edit:
            raise BadRequest('this user has more rights than you')

        user = edit_user_status(id, request.json['status'])

        return jsonify(user.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/users/current', methods=['GET'])
def _get_current_user():
    try:
        current_user_dict = current_user.to_json()

        statuses_to_edit = []
        for status in current_user.get_statuses_to_edit():
            statuses_to_edit.append({'name': get_user_status_title(status), 'value': status})

        current_user_dict['statuses_to_edit'] = statuses_to_edit

        return jsonify(current_user_dict)
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
