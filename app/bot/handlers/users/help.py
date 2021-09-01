from telebot.types import Message

from app.models import User
from ...base import base
from ...helpers import send_message_private
from ...keyboards.inline import get_help_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^🆘 Помощь$')
@bot.message_handler(commands=['help'])
@base()
def help_handler(message: Message, current_user: User):
    text = '\n'.join(
        ('🆘 Информация\n',
         '/info - Узнать информацию по предмету',
         '/schedule - Узнать расписание',
         '/homework - Узнать домашнее задание',
         '/current_info - Определить, сколько времени осталось до конца пары и какая пара будет следующая\n',
         '/help - Помощь по боту',
         '/keyboard - Подключить клавиатуру',
         '/keyboard_off - Отключить клавиатуру\n'))
    reply_markup = None

    if current_user.is_admin():
        text += '\n'.join(
            ('\n👑 Информация для администраторов\n',
             '<i>Домашнее задание можно добавлять по быстрому шаблону</i>',
             '<pre>!Название предмета - задание</pre>\n',
             '/add - Добавить домашнее задание',
             '/edit - Изменить домашнее задание\n',
             '/add_file - Добавить файл в информацию по предмету\n',
             '/users_list - Получить список пользователей\n',
             '/get_id - Получить id сообщения (id прийдет в личку)',
             '/get_file_id - Получить id файла',
             '/delete - Удалить сообщение бота',
             '/call_all - Позвать всех участников группы\n')
        )

    text += '\nСоздатель @briler'
    markup = get_help_inline_markup(current_user.is_admin())

    send_message_private(message, text, reply_markup=markup)
