from telebot.types import BotCommand, BotCommandScopeChat, BotCommandScope

from .admin import get_admin_commands
from ..loader import bot


def get_super_admin_commands(user_id: int, chat_id: int = None) -> list[BotCommand]:
    commands = get_admin_commands(user_id, chat_id)

    if user_id == chat_id:
        return commands

    commands.extend([
        BotCommand('/load_all', 'Добавить всех администраторов чата в базу данных'),
    ])

    return commands


def set_super_admin_commands(user_id: int, chat_id: int = None):
    commands = get_super_admin_commands(user_id, chat_id)

    if user_id == chat_id:
        return bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id))

    bot.set_my_commands(commands, scope=BotCommandScope('chat_member', chat_id, user_id))
