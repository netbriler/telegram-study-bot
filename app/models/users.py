from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(255))
    status = db.Column(db.String(225), default='user')
    photo_id = db.Column(db.String(225))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def is_banned(self) -> bool:
        return self.status == 'banned'

    def is_admin(self) -> bool:
        return self.status in ['admin', 'super_admin']

    def is_super_admin(self) -> bool:
        return self.status == 'super_admin'

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'status': self.status,
            'status_title': get_user_status_title(self.status),
            'photo_id': self.photo_id,
            'created_at': str(self.created_at),
        }
        return json_story

    def get_statuses_to_edit(self):
        statuses_to_edit = []

        if self.is_admin():
            statuses_to_edit.extend(('user', 'banned'))
        if self.is_super_admin():
            statuses_to_edit.extend(('admin', 'super_admin'))

        return statuses_to_edit


def get_user_status_title(status) -> [str, None]:
    status_dict = {
        'user': 'Пользователь',
        'banned': 'Заблокированый',
        'admin': 'Админ',
        'super_admin': 'Супер админ'
    }
    if status in status_dict:
        return status_dict[status]

    return None
