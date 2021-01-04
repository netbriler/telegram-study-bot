from app.utils.logging import file_logger, client_logger
from decouple import config as env_conf
import logging
import pathlib

DIR = pathlib.Path().absolute()


class LocalConfig:
    LOCATE = env_conf('LOCATE', default='ru_RU', cast=str)

    DB_USER = env_conf('DATABASE_USER', default='', cast=str)
    DB_PASSWORD = env_conf('DATABASE_PASS', default='', cast=str)
    DB_HOST = env_conf('DATABASE_HOST', default='database.sqlite3', cast=str)
    DB_PORT = env_conf('DATABASE_PORT', default='', cast=str)
    DB_NAME = env_conf('DATABASE_NAME', default='', cast=str)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_HOST}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    DEBUG = False

    SECRET_KEY = env_conf('SECRET_KEY', cast=str, default='12345')

    TELEGRAM_BOT_TOKEN = env_conf('TELEGRAM_BOT_TOKEN', default='', cast=str)
    TELEGRAM_USE_POTTING = True

    @classmethod
    def init_app(cls, app):
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(file_logger)
        app.logger.addHandler(client_logger)


class Develop:
    LOCATE = env_conf('LOCATE', default='ru_RU', cast=str)

    DB_USER = env_conf('DATABASE_USER', default='', cast=str)
    DB_PASSWORD = env_conf('DATABASE_PASS', default='', cast=str)
    DB_HOST = env_conf('DATABASE_HOST', default='database.sqlite3', cast=str)
    DB_PORT = env_conf('DATABASE_PORT', default='', cast=str)
    DB_NAME = env_conf('DATABASE_NAME', default='', cast=str)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_HOST}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    DEBUG = True

    SECRET_KEY = env_conf('SECRET_KEY', cast=str, default='12345')

    TELEGRAM_BOT_TOKEN = env_conf('TELEGRAM_BOT_TOKEN', default='', cast=str)
    TELEGRAM_USE_POTTING = True

    @staticmethod
    def init_app(app):
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(client_logger)
        app.logger.addHandler(file_logger)


# Create a config dictionary which is used while initiating the application.
# Config that is going to be used will be specified in the .env file
config_dict = {
    'local': LocalConfig,
    'develop': Develop,
}
