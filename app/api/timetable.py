from flask import jsonify, current_app, abort, request

from app.api import api
from app.exceptions import BadRequest
from app.services.subjects import get_subject
from app.services.timetable import get_subjects_by_week, get_subject_timetable, get_timetable, edit_timetable


@api.route('/timetable/', methods=['GET'])
def _get_timetable():
    try:
        timetable = get_timetable()

        return jsonify(timetable)
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/timetable/week/<int:week>', methods=['GET'])
def _get_timetable_by_week(week: int):
    try:
        if 0 > week or week > 52:
            raise BadRequest('invalid week number')

        timetable = get_subjects_by_week(week)

        return jsonify(
            list(map(lambda day: list(map(lambda s: s.to_json(), day)), timetable)))
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/timetable/subject/<string:codename>', methods=['GET'])
def _get_subject_timetable(codename: str):
    try:
        subject = get_subject(codename)
        if not subject:
            raise BadRequest('subject not found')

        subject_timetable = get_subject_timetable(codename)

        return jsonify(subject_timetable)
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/timetable/', methods=['PATCH'])
def _update_timetable():
    try:
        assert request.json

        for day in request.json:
            edit_timetable(day['id'], day['subjects'])

        return jsonify({'ok': True})
    except BadRequest as e:
        abort(400, description=str(e))
    except AssertionError as e:
        abort(400, description='send at least one parameter')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
