import logging
import pathlib
from pathlib import Path

from loguru import logger

log_file_path = Path(__file__).absolute().parent.parent.parent / 'logs/log.out'

logger.add(log_file_path, format='[{time}] [{level}] [{file.name}:{line}] : {message}', level='DEBUG',
           rotation='1 week', compression='zip')


@logger.catch
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())
