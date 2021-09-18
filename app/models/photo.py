from app import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.String(255))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def to_json(self) -> dict:
        json_story = {
            'id': self.id,
            'file_id': self.file_id,
            'task_id': self.task_id,
        }
        return json_story

    def __repr__(self) -> str:
        return f'<Photo [{self.id}]>'
