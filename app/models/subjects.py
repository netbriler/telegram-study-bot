from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Subject(db.Model):
    __tablename__ = 'subjects'

    codename = db.Column(db.String(64), primary_key=True)

    name = db.Column(db.String(255))
    _aliases = db.Column('aliases', db.Text, default='')
    teacher = db.Column(db.String(225), default='')
    audience = db.Column(db.String(225), default='')
    info = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    tasks = db.relationship('Task', backref='subject', lazy=True, cascade='all,delete')
    files = db.relationship('File', backref='subject', lazy=True, cascade='all,delete')

    @hybrid_property
    def aliases(self) -> list:
        aliases = self._aliases.split(',')
        aliases = list(filter(None, map(str.strip, aliases)))
        aliases.append(self.codename)
        aliases.append(self.name)
        return aliases

    @aliases.setter
    def aliases(self, aliases: list or str):
        if type(aliases) == str:
            self._aliases = aliases
        elif type(aliases) == list:
            self._aliases = ','.join(aliases)

    def __repr__(self) -> str:
        return f'<Subject [{self.codename}] {self.name}>'

    def to_json(self) -> dict:
        json_story = {
            'codename': self.codename,
            'name': self.name,
            'teacher': self.teacher
        }
        return json_story

    def to_full_json(self) -> dict:
        json_story = {
            'codename': self.codename,
            'name': self.name,
            'aliases': self._aliases.split(',') if self._aliases else [],
            'teacher': self.teacher,
            'audience': self.audience,
            'info': self.info,
            'created_at': str(self.created_at),
            'files': list(map(lambda f: f.to_json(), self.files))
        }
        return json_story
