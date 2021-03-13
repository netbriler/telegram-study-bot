import logging
import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Logger setup
# Set file paths for logger
log_folder_path = str(Path('logs').absolute())

# Creates logs folder if not existent
if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

log_file_path = os.path.join(log_folder_path, 'log.out')

# Configure logger format
log_fmt = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'

logger_formatter = logging.Formatter(log_fmt)

# Sets up rotating file handler for file output
file_logger = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 10, backupCount=5, encoding='utf-8')
file_logger.setLevel(logging.DEBUG)
file_logger.setFormatter(logger_formatter)

# Set up stream handler for client output
client_logger = StreamHandler()
client_logger.setLevel(logging.INFO)
client_logger.setFormatter(logger_formatter)
