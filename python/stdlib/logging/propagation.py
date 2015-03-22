#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Examining message propagation.
"""

import logging
import logging_tree

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

    # Configure our root logger.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler()
    root_formatter = logging.Formatter(fmt=msgfmt, datefmt=datefmt)
    root_handler.setFormatter(root_formatter)
    root_logger.addHandler(root_handler)
    
    # Configure our '__main__' logger.
    main_logger = logging.getLogger(__name__)

    # While we might assume that this is in an unconfigured state - it's
    # immediately usuable - and the messages are displayed in the same exact
    # format as our root_logger.
    main_logger.info('emitting messages using main_logger')
    genlogs(main_logger)

    # My initial assumption was that we inherited the root's StreamHandler, but
    # if we examine our logger, we don't see any handlers attached to it (and
    # therefore we can't *remove* them).
    num_handlers = len(main_logger.handlers)
    main_logger.info('number of attached handlers: %s' % num_handlers)

    # We can use the logging_tree module to introspect our loggers. And as we
    # can already saw, __main__ has no explicit handlers (or configuration at
    # all).
    logging_tree.printout()

    # Attach a new StreamHandler to our logger.  We can inject extra text into
    # the specific handler using it's formatter to differentiate between the
    # handler objects that are emitting the messages.
    main_handler = logging.StreamHandler()
    main_formatter = logging.Formatter(fmt=msgfmt + ' (main_handler)',
                                       datefmt=datefmt)
    main_handler.setFormatter(main_formatter)
    main_logger.addHandler(main_handler)

    # Emit the test messages ... and now we can see that we're getting
    # duplicates.
    genlogs(main_logger)

    # If we examine the handlers array again, we see that we have exactly
    # 1 attach handler:
    num_handlers = len(main_logger.handlers)
    main_logger.info('number of attached handlers: %s' % num_handlers)

    # The actual reason we're getting duplicate messages is due to 'message
    # propagation', not inheritence. Non-root loggers have a 'propagate'
    # property, which is set to True by default.
    #
    # This was initially confusing to me, because the messages aren't actually
    # "propogating" between loggers (i.e. the logger name for the duplicate
    # messages are all set to __main__), and the __main__ logger isn't actually
    # inheriting it's own copies of it's parents handlers list. What is
    # happening, is that the messages are "passed to the handlers of higher
    # level loggers in addition to any handlers attached to this logger".
    main_logger.propagate = False
    main_logger.info('emitting messages with propagate set to False')
    genlogs(main_logger)
