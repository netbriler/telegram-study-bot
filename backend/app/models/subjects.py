from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db


class Subject(db.Model):
    __tablename__ = 'subjects'

    codename = db.Column(db.String(64), primary_key=True)

    name = db.Column(db.String(255))
    _aliases = db.Column('aliases', db.Text)
    teacher = db.Column(db.String(225))
    info = db.Column(db.Text)
    files = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    tasks = db.relationship('Task', backref='subject', lazy='dynamic')

    @hybrid_property
    def aliases(self) -> list:
        aliases = self._aliases.split(',')
        aliases = list(filter(None, map(str.strip, aliases)))
        aliases.append(self.codename)
        aliases.append(self.name)
        return aliases

    @aliases.setter
    def aliases(self, aliases: list):
        self._aliases = aliases

    def __repr__(self) -> str:
        return f'<Subject {self.name}>'

    def to_dict(self) -> dict:
        json_story = {
            'codename': self.codename,
            'name': self.name,
            'aliases': self._aliases.split(','),
            'teacher': self.teacher,
            'info': self.info,
            'created_at': str(self.created_at),
        }
        return json_story
