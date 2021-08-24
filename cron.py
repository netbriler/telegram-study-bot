import glob
import os

import telebot

from app.services.users import download_user_avatar, get_users, User
from app.utils.logging import logger
from server import app

STATIC_PATH = f'{app.config["APP_DIR"]}/static'

bot = telebot.TeleBot(app.config['TELEGRAM_BOT_TOKEN'], parse_mode='HTML', threaded=False)


def load_new_avatars(users: list[User]):
    for user in users:
        try:
            download_user_avatar(user)
        except:
            continue


def clean_old_avatars(users):
    photos = [user.photo_id for user in users]

    for photo in glob.glob(f'{STATIC_PATH}/pictures/*.jpg'):
        if not os.path.basename(photo)[:-4] in photos:
            app.logger.debug(f'Delete photo {os.path.basename(photo)}')
            os.remove(photo)


def backup_database():
    return os.system(f"mysqldump -u {app.config['DB_USER']} -h {app.config['DB_HOST']} --set-gtid-purged=OFF "
                     f"--no-tablespaces --column-statistics=0 '{app.config['DB_NAME']}' > db-backup.sql")


@logger.catch
def main():
    users = get_users()

    load_new_avatars(users)
    clean_old_avatars(users)

    if app.config['DB_USER'] and app.config['DB_PASSWORD'] and app.config['DB_HOST'] and app.config['DB_NAME']:
        backup_database()


main()
