from flask import jsonify, current_app, abort, request

from app.api import api
from app.exceptions import BadRequest
from app.services.subjects import get_subject, get_all_subjects, edit_subject


@api.route('/subjects', methods=['GET'])
def _get_subjects():
    try:
        subjects = get_all_subjects()
        return jsonify(list(map(lambda s: s.to_json(), subjects)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects/<string:codename>', methods=['GET'])
def _get_subject(codename: str):
    try:
        subject = get_subject(codename)
        if not subject:
            raise BadRequest('subject not found')

        return jsonify(subject.to_full_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects/<string:codename>', methods=['PATCH'])
def _update_subject(codename: str):
    try:
        assert request.json
        assert request.json['name'] or request.json['aliases'] or request.json['info'] \
               or request.json['teacher'] or request.json['audience'] or request.json['files']

        params = {}

        for name in ['name', 'aliases', 'info', 'teacher', 'audience', 'files']:
            if name in request.json:
                params[name] = request.json[name]

        subject = edit_subject(codename, **params)
        if not subject:
            raise BadRequest('subject not found')

        return jsonify(subject.to_full_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except AssertionError as e:
        abort(400, description='send at least one parameter')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects/<string:codename>/tasks', methods=['GET'])
def _get_subject_tasks(codename: str):
    try:
        subject = get_subject(codename)
        if not subject:
            raise BadRequest('subject not found')

        return jsonify(list(map(lambda s: s.to_json(), subject.tasks)))
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
