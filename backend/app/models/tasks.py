from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_codename = db.Column(db.Integer, db.ForeignKey('subjects.codename'))
    date = db.Column(db.Date)
    task = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
