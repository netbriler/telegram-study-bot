from flask import jsonify, current_app, abort, request

from app.exceptions import BadRequest

from app.api import api

from datetime import datetime
from app.services.tasks import get_task, edit_task, get_tasks, get_tasks_by_date, get_tasks_by_week, delete_task, add_task
from app.services.subjects import get_subject


@api.route('/tasks', methods=['GET'])
def _get_tasks():
    try:
        tasks = get_tasks()
        return jsonify(list(map(lambda s: s.to_json(), tasks)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks', methods=['POST'])
def _add_task():
    try:
        data = request.form.to_dict()

        if 'text' not in data or len(data['text'].strip()) < 1:
            raise BadRequest('text is empty')

        if 'subject' not in data or len(data['subject'].strip()) < 1:
            raise BadRequest('subject is empty')

        subject = get_subject(data['subject'])
        if not subject:
            raise BadRequest('subject not found')

        if 'day' in data and not data['day'].isdigit():
            raise BadRequest('day must be integer')

        if 'day' not in data:
            data['day'] = 0

        task = add_task(data['subject'], data['text'], data['day'])
        if not task:
            raise BadRequest('task not found')

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
        if 'text' not in request.form or len(request.form['text'].strip()) < 1:
            raise BadRequest('text is empty')

        task = edit_task(id, request.form['text'])
        if not task:
            raise BadRequest('task not found')

        return jsonify(task.to_json())
    except BadRequest as e:
        abort(400, description=str(e))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/<int:id>', methods=['DELETE'])
def _delete_task(id: int):
    try:
        task = get_task(id)
        if not task:
            raise BadRequest('task not found')

        if delete_task(id):
            return jsonify('')
        else:
            abort(501, 'failed to delete task')
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


