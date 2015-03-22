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

if __name__ == '__main__':
    # The logging.basicConfig function provides a 'convenience' wrapper for
    # configuring the level, and adding StreamHandler & Formatter objects to the
    # root logger.
    logging.basicConfig(level=logging.DEBUG, format=msgfmt, datefmt=datefmt)

    # We can emit messages with the root logger using the logging.<level>
    # functions.
    logging.info('emitting messages using logging.<level>("message")')
    logging.critical('default message')
    logging.error('default message')
    logging.warning('default message')
    logging.info('default message')
    logging.debug('default message')

    # Using logging.log, we can dynamically set the level.
    logging.info('emitting messages using logging.log(level, message)')
    for level in levels:
        logging.log(level=level, msg='default message')

    # We can also use the root logger explicitly via reference. To get our
    # reference to the root logger, we use logging.getLogger(), without
    # specifying a name.
    root_logger = logging.getLogger()

    # And rather than calling 'logging.log', we call 'root.log':
    logging.info('emitting messages using logger.log(level, message)')
    for level in levels:
        root_logger.log(level=level, msg='default message')

    # We can have multiple loggers, allowing us to emit messsages with a single
    # statement to multiple locations in different formats. A common idiom is to
    # use __name__ to dynamically assign the logger's name, based on the context
    # from which it was instantiated.
    main = logging.getLogger(__name__)

    # And rather than calling 'logging.log', we call 'root.log':
    logging.info('emitting messages using a second logger')
    for level in levels:
        main.log(level=level, msg='default message')
