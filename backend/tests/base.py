import urllib
from unittest import TestCase

from datetime import date

from app import create_app, db
from app.models import Subject, User, Task

from app.services.telegram_auth import _generate_hash

from flask_login import login_user, current_user


app = create_app('testing')


class BaseTestCase(TestCase):
    """A base test case."""
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self._app = app
        self._client = app.test_client()

    def create_app(self):
        return app

    @property
    def client(self):
        return self._client

    @property
    def app(self):
        return self._app

    def setUp(self):
        db.create_all()
        db.session.add(Subject(codename='math', name='Математика', _aliases='матеша,матан,алгебра'))
        db.session.add(Subject(codename='history', name='История', _aliases='истор'))

        db.session.add(Task(subject_codename='math', date=date(2020, 3, 4), task='тестовое задание с математики'))

        db.session.add(User(id=45345234, username='admin', name='Админ', status='super_admin'))
        db.session.add(User(id=64564562, username='user', name='Человек', status='user'))
        db.session.commit()

        self.login()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        data = {
            'id': '45345234',
            'first_name': 'Админ',
            'username': 'admin',
            'auth_date': '1609781334'
        }
        data['hash'] = _generate_hash(data, app.config['TELEGRAM_BOT_TOKEN'])

        data = urllib.parse.urlencode(data)

        response = self.client.get('/login_redirect?'+data, content_type='html/text')
        self.assertEqual(response.status_code, 302)
