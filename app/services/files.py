from app import db
from app.models import File


def get_file(id: int) -> File:
    file = File.query.filter_by(id=id).first()
    return file


def get_all_files() -> list[File]:
    files = File.query.all()
    return files


def add_file(title: str, file_id: str, subject_codename: str = None, task_id: int = None) -> File or False:
    file = File(subject_codename=subject_codename, task_id=task_id, title=title, file_id=file_id)

    try:
        db.session.add(file)
        db.session.commit()
    except:
        db.session.rollback()

    return file


def edit_file(id: int, title) -> File or False:
    file = get_file(id)
    if not file:
        return False

    file.title = title

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return file


def delete_file(id: int) -> File or False:
    file = get_file(id)
    if not file:
        return False

    try:
        db.session.delete(file)
        db.session.commit()
    except:
        db.session.rollback()

    return file
