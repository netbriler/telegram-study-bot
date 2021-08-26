from datetime import datetime

from flask import jsonify, current_app, abort, request

from app.api import api
from app.exceptions import BadRequest
from app.services.subjects import get_subject
from app.services.tasks import get_task, edit_task, get_tasks, get_tasks_by_date, get_tasks_by_week, delete_task, \
    create_task, get_tasks_between_date


@api.route('/tasks', methods=['GET'])
def _get_tasks():
    try:
        tasks = get_tasks()
        return jsonify(list(map(lambda s: s.to_json(), tasks)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks', methods=['POST'])
def _create_task():
    try:
        assert request.json
        assert request.json['text'] and request.json['date'] and request.json['subject_codename']

        subject_codename = request.json['subject_codename']
        text = request.json['text']

        subject = get_subject(subject_codename)
        if not subject:
            raise BadRequest('subject not found')

        try:
            date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date must be in the format %Y-%m-%d')

        task = create_task(text, date, subject_codename)

        return jsonify(task.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/<int:id>', methods=['GET'])
def _get_task(id: int):
    try:
        task = get_task(id)
        if not task:
            raise BadRequest('task not found')

        return jsonify(task.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/<int:id>', methods=['PATCH'])
def _update_task(id: int):
    try:
        assert request.json

        text = None
        date = None
        subject_codename = None

        if 'text' in request.json:
            text = request.json['text']

        if 'date' in request.json:
            try:
                date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
            except ValueError:
                raise BadRequest('the date must be in the format %Y-%m-%d')

        if 'subject_codename' in request.json:
            subject_codename = request.json['subject_codename']
            
            subject = get_subject(subject_codename)
            if not subject:
                raise BadRequest('subject not found')

        assert text or date or subject_codename

        task = edit_task(id, text, date, subject_codename=subject_codename)
        if not task:
            raise BadRequest('task not found')

        return jsonify(task.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except AssertionError as e:
        abort(400, description='send at least one parameter')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/<int:id>', methods=['DELETE'])
def _delete_task(id: int):
    try:
        task = get_task(id)
        if not task:
            raise BadRequest('task not found')

        delete_task(id)

        return jsonify({})
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/date/<string:input_date>', methods=['GET'])
def _get_tasks_by_date(input_date: int):
    try:
        try:
            date_to_get = datetime.strptime(input_date, '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date must be in the format %Y-%m-%d')

        tasks = get_tasks_by_date(date_to_get)

        return jsonify(list(map(lambda s: s.to_json(), tasks)))
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/week/<int:week>', methods=['GET'])
def _get_tasks_by_week(week: int):
    try:
        if 0 > week or week > 52:
            raise BadRequest('invalid week number')

        tasks = get_tasks_by_week(week)

        return jsonify(
            list(map(lambda day: list(map(lambda s: s.to_json(), day)), tasks)))
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/calendar', methods=['GET'])
def _get_tasks_calendar():
    try:
        try:
            date_start = datetime.strptime(request.args.get('date_start'), '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date_start must be in the format %Y-%m-%d')

        try:
            date_end = datetime.strptime(request.args.get('date_end'), '%Y-%m-%d').date()
        except ValueError:
            raise BadRequest('the date_end must be in the format %Y-%m-%d')

        tasks = get_tasks_between_date(date_start, date_end)

        calendar = []
        for task in tasks:
            calendar.append({
                'id': task.id,
                'title': task.subject.name,
                'start': task.date.strftime('%Y-%m-%d'),
                'allDay': True
            })

        return jsonify(calendar)
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
