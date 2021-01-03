from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_codename = db.Column(db.String(64), db.ForeignKey('subjects.codename'))
    date = db.Column(db.Date)
    task = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Task {self.subject_codename}>'

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'subject_codename': self.subject_codename,
            'date': str(self.date),
            'task': self.task,
            'created_at': str(self.created_at),
        }
        return json_story
