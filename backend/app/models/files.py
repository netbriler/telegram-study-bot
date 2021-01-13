from app import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    file_id = db.Column(db.String(255))
    subject_codename = db.Column(db.String(64), db.ForeignKey('subjects.codename'))

    def __repr__(self) -> str:
        return f'<Timetable {self.id} {self.is_work_day}>'
