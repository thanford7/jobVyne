import logging
import sys


LOGGER_NAME = 'defaultLogger'


def setLogger(logLevel=logging.INFO):
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logLevel)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def getLogger():
    return logging.getLogger(LOGGER_NAME)
