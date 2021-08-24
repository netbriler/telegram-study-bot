from telebot.types import BotCommandScopeDefault, BotCommand

from ..loader import bot


def get_default_commands() -> list[BotCommand]:
    commands = [
        BotCommand('/info', 'Узнать информацию по предмету'),
        BotCommand('/schedule', 'Узнать расписание'),
        BotCommand('/homework', 'Узнать домашнее задание'),
        BotCommand('/current_info', 'Определить, сколько времени осталось до конца пары и какая пара будет следующая'),
        BotCommand('/help', 'Помощь по боту'),
        BotCommand('/keyboard', 'Подключить клавиатуру'),
        BotCommand('/keyboard_off', 'Отключить клавиатуру'),
    ]

    return commands


def set_default_commands():
    commands = get_default_commands()

    bot.set_my_commands(commands, scope=BotCommandScopeDefault())
