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
    for level in levels:
        logger.log(level=level, msg=msg)

class ColorFormatter(logging.Formatter):

    # ASCII escapes.
    reset   = '\x1b[0m'
    bold    = '\x1b[1m'
    black   = '\x1b[30m'
    red     = '\x1b[31m'
    green   = '\x1b[32m'
    yellow  = '\x1b[33m'
    blue    = '\x1b[34m'
    magenta = '\x1b[35m'
    cyan    = '\x1b[36m'
    white   = '\x1b[37m'

    # Bind ASCII color escapes to standard log levels.
    color_level = {
        logging.CRITICAL: red + bold,
        logging.ERROR:    red,
        logging.WARNING:  yellow,
        logging.INFO:     green,
        logging.DEBUG:    magenta
    }

    def __init__(self, fmt=None, datefmt=None, default_color=cyan):
        """ ColorFormatter constructor.

        Piggybacks off the default Formatter constructor. Allows user to set
        a default_color if desired. Defaults to 'cyan'.
        """
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)
        self.default_color = default_color

    def format(self, record):
        """ Format log messages.

        Piggybacks off the default format method. Injects color escapes
        & resets, based on the log level.
        """
        message = logging.Formatter.format(self, record)

        try:
            color = ColorFormatter.color_level[record.levelno]
        except:
            color = self.default_color

        message = color + message + ColorFormatter.reset
        return message

if __name__ == '__main__':

    # Setup logger using the color formatter.    
    color_logger = logging.getLogger('color_logger')
    color_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = ColorFormatter(fmt=msgfmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    color_logger.addHandler(handler)

    # Emit test messages using standard levels.
    genlogs(color_logger)

    # Emit test message using an undefined level.
    color_logger.log(level=99, msg='default message')



