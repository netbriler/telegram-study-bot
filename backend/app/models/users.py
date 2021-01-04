from flask_login import UserMixin
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(255))
    status = db.Column(db.String(225), default='user')
    photo_id = db.Column(db.String(225))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def is_admin(self) -> bool:
        return self.status in ['admin', 'super_admin']

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'status': self.status,
            'photo_id': self.photo_id,
            'created_at': str(self.created_at),
        }
        return json_story
