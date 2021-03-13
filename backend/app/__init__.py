import locale

from config import config_dict
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_key: str = 'local') -> Flask:
    app = Flask(__name__, static_url_path='/static')
    app.app_context().push()

    app.config.from_object(config_dict[config_key])
    config_dict[config_key].init_app(app)

    locale.setlocale(locale.LC_ALL, app.config['LOCATE'])

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main import main as main_blueprint
    from app.api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
