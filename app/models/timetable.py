from app import db


class Timetable(db.Model):
    __tablename__ = 'timetable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subjects = db.Column(db.Text)
    is_work_day = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'<Timetable {self.id} {self.is_work_day}>'


def init_timetable():
    if not Timetable.query.all():
        for i in range(14):
            db.session.add(Timetable(subjects=''))
        db.session.commit()
