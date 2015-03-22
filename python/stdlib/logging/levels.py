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
    # Apply a basic configuratin to the root logger.
    logging.basicConfig(level=logging.DEBUG, format=msgfmt, datefmt=datefmt)

    # The logging levels are just integers, mapped to properties in the logging
    # module. We can create our own by assigning an integer to a module-level
    # property and giving it a name:
    logging.USER = 99
    logging.addLevelName(logging.USER, 'USER')

    # And insert it into our 'levels' array.
    levels.insert(0, logging.USER)

    # Enumerate our levels, and display the integer value for each level.
    for level in levels:
        logging.log(level=level, msg='level as integer: %s' % level)

