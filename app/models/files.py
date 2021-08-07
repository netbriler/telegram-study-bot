from app import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    file_id = db.Column(db.String(255))
    subject_codename = db.Column(db.String(64), db.ForeignKey('subjects.codename'))

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'title': self.title,
            'file_id': self.file_id,
        }
        return json_story

    def __repr__(self) -> str:
        return f'<Timetable {self.id} {self.is_work_day}>'
