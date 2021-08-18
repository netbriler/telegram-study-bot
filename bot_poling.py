from decouple import config
from flask_migrate import Migrate

from app import create_app, db

env_config = config('ENV', cast=str, default='develop')

app = create_app(env_config)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    from app.models import init_models

    init_models()

if __name__ == '__main__':
    with app.app_context():
        from app.bot import bot

        bot.polling()
