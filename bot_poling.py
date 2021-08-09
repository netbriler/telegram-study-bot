from decouple import config

from app import create_app
from app.bot import bot

env_config = config('ENV', cast=str, default='develop')

app = create_app(env_config)

if __name__ == '__main__':
    with app.app_context():
        bot.polling()
