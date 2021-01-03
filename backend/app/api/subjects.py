from flask import jsonify, request, current_app, abort

from app.models import Subject, Task
from app.api import api
from app import db


@api.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        subjects = Subject.query.all()
        return jsonify(list(map(lambda s: s.to_json(), subjects)))
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects/<string:codename>', methods=['GET'])
def get_subject(codename: str):
    try:
        subject = Subject.query.filter_by(codename=codename).first()
        if not subject:
            raise ValueError

        return jsonify(subject.to_json())
    except ValueError:
        abort(400, description='Bad Request: subject not found')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')


@api.route('/subjects/<string:codename>/tasks', methods=['GET'])
def get_tasks_by_subject(codename: str):
    try:
        subject = Subject.query.filter_by(codename=codename).first()
        if not subject:
            raise ValueError

        return jsonify(list(map(lambda s: s.to_json(), subject.tasks)))
    except ValueError:
        abort(400, description='Bad Request: subject not found')
    except Exception as e:
        current_app.logger.error(e)
        abort(500, description='Server error')
