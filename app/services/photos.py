from app import db
from app.models import Photo


def get_photo(id: int) -> Photo:
    photo = Photo.query.filter_by(id=id).first()
    return photo


def get_all_task_photos(task_id: int) -> list[Photo]:
    files = Photo.query.filter_by(task_id=task_id).all()
    return files


def add_photo(file_id: str, task_id: int) -> Photo or False:
    photo = Photo(file_id=file_id, task_id=task_id)

    try:
        db.session.add(photo)
        db.session.commit()
    except:
        db.session.rollback()

    return photo


def add_photos(photos: list[str], task_id: int) -> Photo or False:
    for file_id in photos:
        add_photo(file_id, task_id)

    return True


def delete_photo(id: str) -> Photo or False:
    photo = get_photo(id)
    if not photo:
        return False

    try:
        db.session.delete(photo)
        db.session.commit()
    except:
        db.session.rollback()

    return photo
