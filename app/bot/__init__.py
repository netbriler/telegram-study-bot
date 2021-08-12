from .handlers import bot


def init_bot():
    from .commands import set_default_commands

    set_default_commands()


init_bot()
