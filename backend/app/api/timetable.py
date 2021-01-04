from flask import jsonify, current_app, abort

from app.api import api

from datetime import datetime
from app.services.timetable import get_subjects_by_date, get_subjects_by_week


@api.route('/timetable/<string:input_date>', methods=['GET'])
def _get_timetable_by_date(input_date: str):
    try:
        date_to_get = datetime.strptime(input_date, '%Y-%m-%d').date()
        subjects = get_subjects_by_date(date_to_get)
        assert subjects

        return jsonify(list(map(lambda s: s.to_json(), subjects)))
    except ValueError:
        abort(400, description='Bad Request: the date must be in the format %Y-%m-%d')
    except AssertionError:
        abort(404, description='Not Found: there are no subjects on this date')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/timetable/week/<int:week>', methods=['GET'])
def _get_timetable_by_week(week: int):
    try:
        timetable = get_subjects_by_week(week)
        assert timetable

        return jsonify(
            list(map(lambda day: {**day, 'subjects': list(map(lambda s: s.to_json(), day['subjects']))}, timetable)))
    except ValueError:
        abort(400, description='Bad Request: wrong week number')
    except AssertionError:
        abort(404, description='Not Found: there are no subjects on this date')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')

