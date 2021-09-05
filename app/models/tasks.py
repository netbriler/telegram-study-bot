from datetime import datetime

from app import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_codename = db.Column(db.String(64), db.ForeignKey('subjects.codename'))
    date = db.Column(db.Date)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    files = db.relationship('File', backref='task', lazy=True, cascade='all,delete')

    def __repr__(self) -> str:
        return f'<Task [{self.id}] {self.subject_codename}>'

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'subject': self.subject.to_json(),
            'date': str(self.date),
            'text': self.text,
            'created_at': str(self.created_at),
            'files': list(map(lambda f: f.to_json(), self.files))
        }
        return json_story
