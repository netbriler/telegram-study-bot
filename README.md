# Как установить?

## Клонировать собраную версию бота

`git clone --single-branch --branch build https://github.com/netbriler/telegram-study-bot.git`

## Установить зависимости

`cd telegram-study-bot` - _заходим в папку с ботом_

`python3.9 -m pip install -r requirements.txt --user`

## Настроить переменные окружения
`cp .env.template .env` - копирует файл `.env.template` в `.env` уже без окончания `.template`

В файле `.env` указать:
* Токен бота
* Доступы к базе данных
* Базовые настройки


### Бот поддерживает 2 базы данных
* mysql
* sqlite (чуть по медленее)

Если использовать `mysql` не судьба, то переменные осталяем пустыми, а вместо хоста базы даных пишем название файла sqlite
`DATABASE_HOST=database.sqlite3`

# Стартуем бота
*Есть 2 способа запустить бота*

## 1. Webhook
_Этим способом ботов запускают уже в боевых условиях_

- `python3.9 server.py` - запускает админку и бота с webhook
- переходим по ссылке `https://[тут ваш домен]/setWebhook` чтобы подключить webhook бота к вашему серверу

## 2. Polling
`python3.9 bot_poling.py` - запускает только бота через pooling.

_Отличный вариант для тестирование, но на продакшине лучше использовать webhook_
