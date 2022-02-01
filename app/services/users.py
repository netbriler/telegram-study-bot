import requests
from flask import current_app

from app import db
from app.models import User


def get_user(id: int) -> [User, None]:
    user = User.query.filter_by(id=id).first()

    if not user:
        return None

    return user


def get_users() -> list[User]:
    users = User.query.all()

    return users


def create_user(id: int, name, username=None) -> [User, None]:
    user = User(id=id, name=name, username=username)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()

    return user


def edit_user(id: int, name, username=None) -> [User, None]:
    user = get_user(id)
    if not user:
        return None

    user.name = name
    user.username = username

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return user


def edit_user_status(id: int, status: str) -> [User, None]:
    user = get_user(id)
    if not user:
        return None

    user.status = status

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return user


def get_or_create_user(id: int, name: str, username: str) -> User:
    user = get_user(id)

    if not user:
        return create_user(id, name, username)
    else:
        user = edit_user(id, name, username)

    return user


def download_user_avatar(user: User, bot):
    photos = bot.get_user_profile_photos(user.id).photos

    if len(photos) > 0:
        photo_id = photos[0][-1].file_id

        if photo_id and user.photo_id != photo_id:
            r = requests.get(bot.get_file_url(photo_id), allow_redirects=True)
            open(f'{current_app.config["APP_DIR"]}/static/pictures/{photo_id}.jpg', 'wb').write(r.content)

            user.photo_id = photo_id

            try:
                db.session.commit()
            except:
                db.session.rollback()


def count_users() -> int:
    return User.query.count()
