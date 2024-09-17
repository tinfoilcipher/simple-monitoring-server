import logging
import logging.handlers
from os import environ
from sys import stdout
from datetime import datetime

def log_builder(config):
    
    #--Root Logger
    logger = logging.getLogger()
    logger.setLevel(config["level"])
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    #--Log File, 20MB Rotating
    file_handler = logging.handlers.RotatingFileHandler(config["file_path"],
                                                        mode="a",
                                                        maxBytes=20*1024*1024,
                                                        encoding='utf-8')
    file_handler.setLevel(config["level"])
    file_handler.setFormatter(formatter)

    #--STDOUT
    stream_handler = logging.StreamHandler(stream=stdout)
    stream_handler.setLevel(config["stream_level"])
    stream_handler.setFormatter(formatter)

    #--Ensure we don't make an infinite amount of handlers
    if not len(logger.handlers):
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
    
def log_writer(logline, config):
    logger = log_builder(config)
    #--Catch all offlines as ERRORs
    if "offline" in logline:
        logger.error(logline)
    elif "error" in logline:
        logger.error(logline)
    elif "Email Alert" in logline:
        logger.warning(logline)
    else:
        logger.info(logline)
