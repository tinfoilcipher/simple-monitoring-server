import logging
import logging.handlers
from sys import stdout
from datetime import datetime

def log_builder():
    
    #--Root Logger
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    #--Log File, 20MB Rotating
    file_handler = logging.handlers.RotatingFileHandler("monitor.log",
                                                        mode="a",
                                                        maxBytes=20*1024*1024,
                                                        encoding='utf-8')
    file_handler.setLevel("DEBUG")
    file_handler.setFormatter(formatter)

    #--STDOUT
    stream_handler = logging.StreamHandler(stream=stdout)
    stream_handler.setLevel("INFO")
    stream_handler.setFormatter(formatter)

    #--Ensure we don't make an infinite amount of handlers
    if not len(logger.handlers):
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
    
def log_writer(logline):
    logger = log_builder()
    #--Catch all offlines as ERRORs
    if "online" not in logline:
        logger.error(logline)
    elif "Raising Alert" in logline:
        logger.warning(logline)
    else:
        logger.info(logline)
