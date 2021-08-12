from telebot.types import BotCommandScopeChat, BotCommandScope

from ..loader import bot


def delete_admin_commands(user_id: int, chat_id: int = None):
    bot.delete_my_commands(BotCommandScopeChat(user_id))
    if chat_id != user_id:
        bot.delete_my_commands(BotCommandScope('chat_member', chat_id, user_id))
