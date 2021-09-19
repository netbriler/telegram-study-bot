from ..loader import bot
from app.utils.logging import logger


def save_delete_message(chat_id: int, message_id: int):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        logger.warning(f'Error when deleting message: {message_id} in chat: {chat_id}')
