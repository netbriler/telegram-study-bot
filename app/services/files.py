from app import db
from app.models import File


def get_file(id: int) -> File:
    file = File.query.filter_by(id=id).first()
    return file


def get_all_files() -> list[File]:
    files = File.query.all()
    return files


def add_file(subject_codename: str, title: str, file_id: str) -> File or False:
    file = File(subject_codename=subject_codename, title=title, file_id=file_id)

    db.session.add(file)
    db.session.commit()

    return file
