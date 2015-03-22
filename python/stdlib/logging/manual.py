#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manual configure loggers without basicConfig.
"""

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

if __name__ == '__main__':
    # Get the 'root' logger.
    root_logger = logging.getLogger()

    # Set the level on the *LOGGER*. By default this is set to logging.ERROR,
    # limiting the messages recieved by the logger.
    root_logger.setLevel(logging.DEBUG)

    # Instead of using basicConfig, we can manually configure our own handlers.
    # A logger can have multiple handlers (this is why basicConfig requires
    # a *list* of handlers, even if we're only using one. The handler inherits
    # the loggers configured level, but can also be adjusted filter the messages
    # at the handler as well.
    root_handler = logging.StreamHandler()

    # Each handler has it's own 'formatter' object, allowing the emitting
    # messages to be transformed 'per-destintation'. We create the formatter,
    # then set it on the handler.
    root_formatter = logging.Formatter(fmt=msgfmt, datefmt=datefmt)
    root_handler.setFormatter(root_formatter)

    # And finally, add the handler to the logger to 'enable' it.
    root_logger.addHandler(root_handler)
    
    # Emit some example log messages.  We can send emit messages using
    # a specific logger.
    root_logger.info('emitting messages using the root_logger')
    genlogs(root_logger)

    # Create a second logger & emit messages. Note: main_logger hasn't been
    # configured and doesn't have its own handler. See 'propagation.py' for an
    # explanation of this behavior.
    main_logger = logging.getLogger(__name__)
    main_logger.info('emitting messages using the main_logger')
    genlogs(main_logger)
