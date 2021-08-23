## Как установить?

### 1. Клонировать собраную версию бота

`git clone --single-branch --branch build https://github.com/netbriler/telegram-study-bot.git`

### 2. Установить зависимости

`python3.9 -m pip install -r requirements.txt`

### 3. Настроить переменные окружения
`cp .env.dist .env` - копирует файл `.env.dist` в `.env`

В файле `.env` указать:
* Токен бота
* Доступы к базе данных
* Базовые настройки


#### Бот поддерживает 2 базы данных
* mysql
* sqlite (чуть по медленее)

Если использовать `mysql` не судьба, то переменные осталяем пустыми, а вместо хоста базы даных пишем название файла sqlite
`DATABASE_HOST=database.sqlite3`

### 4. Стартуем бота
`python3.9 app.py`
