from app.models import User

from app import db


def get_user(id: int) -> User:
    user = User.query.filter_by(id=id).first()

    if not user:
        return None

    return user


def get_users() -> list[User]:
    users = User.query.all()

    return users


def create_user(id: int, name, username=None, photo_id=None) -> User:
    user = User(id=id, name=name, username=username, photo_id=photo_id)

    db.session.add(user)
    db.session.commit()

    return user


def edit_user(id: int, name, username=None, photo_id=None) -> User:
    user = get_user(id)
    if not user:
        return None

    user.name = name
    user.username = username
    user.photo_id = photo_id

    db.session.commit()

    return user
