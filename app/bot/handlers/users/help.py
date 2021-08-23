from telebot.types import Message

from app.models import User
from ...base import base
from ...helpers import send_message_private
from ...loader import bot


@bot.message_handler(regexp='^🆘 Помощь$')
@bot.message_handler(commands=['help'])
@base()
def help_handler(message: Message, current_user: User):
    text = '\n'.join(
        ('🆘 Информация 🆘\n',
         '/info - Узнать информацию по предмету',
         '/schedule - Узнать расписание',
         '/homework - Узнать ДЗ',
         '/current_info - Определить, сколько времени осталось до конца пары и какая пара будет следующая\n',
         '/help - Помощь по боту',
         '/keyboard - Подключить клавиатуру',
         '/keyboard_off - Отключить клавиатуру\n'))

    if current_user.is_admin():
        text += '\n'.join(
            ('👑 Информация для администраторов 👑\n',
             '<i>ДЗ можно добавлять по быстрому шаблону</i>',
             '<pre>!Название предмета - задание</pre>\n',
             '/add - Добавить ДЗ',
             '/edit - Изменить ДЗ\n',
             '/add_file - Добавить файл в информацию по предмету\n',
             '/users_list - Получить список пользователей\n',
             '/get_id - Получить id сообщения (id прийдет в личку)',
             '/get_file_id - Получить id файла',
             '/delete - Удалить сообщение бота',
             '/call_all - Позвать всех участников группы\n')
        )

    text += '\nСоздатель @briler'

    send_message_private(message, text)
