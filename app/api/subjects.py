from flask import jsonify, current_app, abort, request

from app.api import api
from app.exceptions import BadRequest, Conflict
from app.services.subjects import get_subject, get_all_subjects, create_subject, edit_subject, delete_subject, \
    get_none_subject
from app.services.timetable import delete_subject_from_timetable


@api.route('/subjects', methods=['GET'])
def _get_subjects():
    try:
        subjects = get_all_subjects()
        if request.args.get('with_none_subject'):
            subjects.append(get_none_subject())

        return jsonify(list(map(lambda s: s.to_json(), subjects)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects', methods=['POST'])
def _create_subject():
    try:
        assert request.json
        assert request.json['name'] or request.json['codename'] or request.json['aliases'] or request.json['info'] \
               or request.json['teacher'] or request.json['audience'] or request.json['files']

        if get_subject(request.json['codename']):
            raise Conflict(f'subject with codename {request.json["codename"]} already exists')

        params = {}

        for name in ['codename', 'name', 'aliases', 'info', 'teacher', 'audience', 'files']:
            if name in request.json:
                params[name] = request.json[name]

        subject = create_subject(**params)
        if not subject:
            raise BadRequest('subject not found')

        return jsonify(subject.to_full_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Conflict as e:
        abort(409, description=str(e))
    except AssertionError as e:
        abort(400, description='send at least one parameter')
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


@api.route('/subjects/<string:codename>', methods=['DELETE'])
def _delete_subject(codename: str):
    try:
        subject = delete_subject(codename)
        if not subject:
            raise BadRequest('subject not found')

        delete_subject_from_timetable(codename)

        return jsonify({})
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
