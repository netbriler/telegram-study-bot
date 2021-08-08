from datetime import datetime

from flask import jsonify, current_app, abort

from app.api import api
from app.exceptions import BadRequest
from app.services.subjects import get_subject
from app.services.timetable import get_subjects_by_date, get_subjects_by_week, get_subject_timetable


@api.route('/timetable/<string:input_date>', methods=['GET'])
def _get_timetable_by_date(input_date: str):
    try:
        try:
            date_to_get = datetime.strptime(input_date, '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date must be in the format %Y-%m-%d')

        subjects = get_subjects_by_date(date_to_get)
        if not subjects:
            raise BadRequest('there are no subjects on this date')

        return jsonify(list(map(lambda s: s.to_json(), subjects)))
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
