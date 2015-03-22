#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


# 'Standard' date & message format strings.
msgfmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
datefmt = '%H:%M:%S'

# A list containing the standard levels.
levels = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
]

def genlogs(logger, msg='default message'):
    """ Emit test log messages for each level.
    
    Generates a test message for each standard logging level using the specified
    logger object.

    Args: 
        logger: A logger object.
        message: The message to display.
    Returns: None
    """
    # for x in range(0, 100):
    #     level = logging.getLevelName(x)
    #     print(level)

    for level in levels:
        logger.log(level=level, msg=msg)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        message = logging.Formatter.format(self, record)
        message = message + ' (custom formatter)'
        return message

class CustomStreamHandler(logging.StreamHandler):
    def emit(self, record):
        record.msg = record.msg + ' (custom handler)'
        logging.StreamHandler.emit(self, record)

if __name__ == '__main__':

    # Logging with a customer formatter.
    cf_logger = logging.getLogger('custom_formatter')
    cf_logger.setLevel(logging.DEBUG)
    cf_handler = logging.StreamHandler()
    cf_formatter = CustomFormatter(fmt=msgfmt, datefmt=datefmt)
    cf_handler.setFormatter(cf_formatter)
    cf_logger.addHandler(cf_handler)
    genlogs(cf_logger)

    # Logging with a custom handler.
    ch_logger = logging.getLogger('custom_handler')
    ch_logger.setLevel(logging.DEBUG)
    ch_handler = CustomStreamHandler()
    ch_formatter = logging.Formatter(fmt=msgfmt, datefmt=datefmt)
    ch_handler.setFormatter(ch_formatter)
    ch_logger.addHandler(ch_handler)
    genlogs(ch_logger)



