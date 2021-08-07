from app.models import User
from telebot.types import Message

from ...base import base
from ...loader import bot
from ...utils import send_message_private


@bot.message_handler(regexp='^🆘Помощь🆘$')
@bot.message_handler(commands=['help'])
@base()
def help_handler(message: Message, current_user: User):
    text = """    
🆘 Информация 🆘

/info - Узнать информацию по предмету
/schedule - Узнать расписание
/homework - Узнать ДЗ
/current_info - Определить, сколько времени осталось до конца пары и какая пара будет следующая

/help - Помощь по боту
/keyboard - Подключить клавиатуру
/keyboard_off - Отключить клавиатуру
"""
    if current_user.is_admin():
        text += """
👑 Информация для администраторов 👑

<i>ДЗ можно добавлять по быстрому шаблону</i>
<pre>!Название предмета - задание</pre>

/add - Добавить ДЗ
/edit - Изменить ДЗ

/users_list - Получить список пользователей

/get_id - Получить id сообщения (id прийдет в личку)
/get_file_id - Получить id файла
/delete - Удалить сообщение бота
/call_all - Позвать всех участников группы
"""

    text += '\nСоздатель @briler'

    send_message_private(message, text)
