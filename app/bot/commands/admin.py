from telebot.types import BotCommand, BotCommandScopeChat, BotCommandScope

from .default import get_default_commands
from ..loader import bot


def get_admin_commands(user_id: int, chat_id: int = None) -> list[BotCommand]:
    commands = get_default_commands()

    commands.extend([
        BotCommand('/add', 'Добавить домашнее задание'),
        BotCommand('/edit', 'Изменить домашнее задание'),
        BotCommand('/add_file', 'Добавить файл в информацию по предмету'),
        BotCommand('/users_list', 'Получить список пользователей'),
        BotCommand('/get_file_id', 'Получить id файла'),
        BotCommand('/cancel', 'Отменить текущее действие'),
    ])

    if user_id == chat_id:
        return commands

    commands.extend([
        BotCommand('/get_id', 'Получить id сообщения (id прийдет в личку)'),
        BotCommand('/delete', 'Удалить сообщение бота'),
        BotCommand('/call_all', 'Позвать всех участников группы')
    ])

    return commands


def set_admin_commands(user_id: int, chat_id: int = None):
    commands = get_admin_commands(user_id, chat_id)

    if user_id == chat_id:
        return bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id))

    bot.set_my_commands(commands, scope=BotCommandScope('chat_member', chat_id, user_id))
