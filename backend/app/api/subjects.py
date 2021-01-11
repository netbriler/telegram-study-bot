from flask import jsonify, current_app, abort

from app.exceptions import BadRequest

from app.api import api

from app.services.subjects import get_subject, get_all_subjects


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

        return jsonify(subject.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
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
