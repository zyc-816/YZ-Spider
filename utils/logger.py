import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import config


class ColoredFormatter(logging.Formatter):
    COLOR_RESET = "\033[0m"
    def format(self, record: logging.LogRecord) -> str:
        color = config.COLOR_MAP.get(record.levelno, self.COLOR_RESET)
        return f"{color}{super().format(record)}{self.COLOR_RESET}"
    
def setup_logger(name: str = "logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if(logger.hasHandlers()):
        return logger

    # set log level
    level = getattr(logging, config.FILE_LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    # set format
    log_format = "[%(asctime)s][%(levelname)-7s][%(filename)s:%(lineno)d]: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.CONSOLE_LOG_LEVEL)
    console_handler.setFormatter(ColoredFormatter(log_format, datefmt=date_format))
    logger.addHandler(console_handler)

    # file handler
    os.makedirs(config.LOG_FILE.parent, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        filename=config.LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=config.LOG_BACKUP_DAYS,
        encoding="utf-8"
    )
    file_handler.setLevel(config.FILE_LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()