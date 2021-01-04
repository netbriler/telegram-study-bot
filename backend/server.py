from flask_migrate import Migrate, upgrade
from app import create_app, db
from decouple import config

env_config = config('ENV', cast=str, default='develop')

app = create_app(env_config)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
