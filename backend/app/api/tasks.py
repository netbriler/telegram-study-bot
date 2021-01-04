from flask import jsonify, current_app, abort

from app.models import Task
from app.api import api


@api.route('/tasks', methods=['GET'])
def _get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify(list(map(lambda s: s.to_json(), tasks)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/tasks/<int:id>', methods=['GET'])
def _get_task(id: int):
    try:
        task = Task.query.filter_by(id=id).first()
        if not task:
            raise ValueError

        return jsonify(task.to_json())
    except ValueError:
        abort(400, description='Bad Request: task not found')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
