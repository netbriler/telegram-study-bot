import requests
from app.bot.loader import app, bot
from app.services.users import get_user, create_user, edit_user


def base(admin=False, callback_query=False):

    def error_boundary(func):

        def wrapper(message):
            try:
                with app.app_context():
                    id = message.from_user.id
                    user = get_user(id)

                    name = message.from_user.first_name
                    if message.from_user.last_name:
                        name += ' ' + message.from_user.last_name

                    username = message.from_user.username

                    photo_id = None

                    photos = bot.get_user_profile_photos(id).photos
                    if len(photos) > 0:
                        photo_id = photos[0][-1].file_id

                    if not user or user.photo_id != photo_id:
                        r = requests.get(bot.get_file_url(photo_id), allow_redirects=True)
                        open(f'{app.config["APP_DIR"]}/static/pictures/{photo_id}.jpg', 'wb').write(r.content)

                    if not user:
                        user = create_user(id, name, username, photo_id)
                    else:
                        user = edit_user(id, name, username, photo_id)

                    return func(message, user)

            except Exception as e:
                app.logger.error(e)

        return wrapper

    return error_boundary
