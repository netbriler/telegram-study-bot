import json

import requests
from decouple import config

api_token = config('TELEGRAM_BOT_TOKEN', default='', cast=str)

last_update = 0

while True:
    r = requests.get(f'https://api.telegram.org/bot{api_token}/getUpdates?offset=-1')
    data = r.json()['result']

    if len(data) > 0:
        update = data[0]
    else:
        continue

    if last_update == update['update_id']:
        continue

    print(update)

    last_update = update['update_id']

    requests.post(f'http://127.0.0.1:5000/{api_token}', data=json.dumps(update))
