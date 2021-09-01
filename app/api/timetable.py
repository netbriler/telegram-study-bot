from datetime import datetime

from flask import jsonify, current_app, abort, request
from flask_login import current_user

from app.api import api
from app.exceptions import BadRequest
from app.services.subjects import get_subject, get_all_subjects, get_none_subject
from app.services.timetable import get_subjects_by_date, get_subject_timetable, get_timetable, edit_timetable
from app.utils.logging import logger


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


@api.route('/timetable/date/<string:date>', methods=['GET'])
def _get_timetable_by_date(date: str):
    try:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date_start must be in the format %Y-%m-%d')

        timetable = get_subjects_by_date(date,
                                         with_none_subject=False if request.args.get('without_none_subject') else True)

        return jsonify(list(map(lambda s: s.to_json(), timetable)))
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
        assert request.json['timetable']

        subjects = get_all_subjects()
        subjects.append(get_none_subject())
        subject_codename_list = [s.codename for s in subjects]

        for day in request.json['timetable']:
            if day['subjects']:
                for subject in day['subjects'].split(','):
                    if subject not in subject_codename_list:
                        raise BadRequest(f'subject "{subject}" not found')

            edit_timetable(day['id'], day['subjects'])

        logger.info(f'{current_user} edited timetable')

        return jsonify({'ok': True})
    except BadRequest as e:
        abort(400, description=str(e))
    except AssertionError as e:
        abort(400, description='send at least one parameter')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
