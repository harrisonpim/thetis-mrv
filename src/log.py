import sys
from logging import Logger

from loguru import logger


def get_logger() -> Logger:
    """remove the default logger and return one with nice formatting"""
    logger.remove()
    logger.add(sys.stderr, format="{time} | {level} | {message} | {extra}")
    return logger
