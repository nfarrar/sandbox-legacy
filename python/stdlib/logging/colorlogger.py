#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Nathan Farrar"
__website__ = "http://crunk.io"
__email__ = "nfarrar@crunk.io"
__version__ = 0.1

import logging
import sys


class ColorFormatter(logging.Formatter):
    """ ColorFormatter with defaults & color injection. """

    def __init__(self, fmt='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                 datefmt='%H:%M:%S', reset='\x1b[0m'):
        """ Better defaults for fmt & datefmt. Posix ANSI escape for terminal
        property reset can be overriden if necessary. """
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)
        self.reset = reset

    def format(self, record):
        """ Inject colors into log record. """
        message = logging.Formatter.format(self, record)

        try:
            color = logging._levelColors[record.levelno]
            message = color + message + self.reset
        except:
            pass

        return message

class ColorStreamHandler(logging.StreamHandler):
    """ StreamHandler with better defaults. """

    def __init__(self, level=logging.DEBUG, stream=sys.stderr, 
                 formatter=ColorFormatter()):
        """ Sets the handler level to DEBUG (rather than ERROR) by default. Uses
        stderr instead of stdout. Binds the ColorFormatter if another Formatter
        hasn't been provided. """
        logging.StreamHandler.__init__(self, stream=stream)

        if formatter is not None:
            self.setFormatter(formatter)

class ColorLogger(logging.getLoggerClass()):
    """ A ColorLogger class with default colormap and convenience methods. """

    def __init__(self, name, level=logging.DEBUG, propagate=False,
                 handlers=[ColorStreamHandler()],
                 colormap={50: '\x1b[1;31m',        # bold red
                           40: '\x1b[31m',          # red
                           30: '\x1b[33m',          # yellow
                           20: '\x1b[32m',          # green
                           10: '\x1b[35m'}):        # magenta
        """ Sets the logger level to logging.DEBUG rather than logging.ERROR by
        default. Disables message propogation. Uses the ColorStreamHandler if
        another handler hasn't been provided. Sets a default colormap. """

        # If logging._levelColors is not defined, define it.
        try:
            colors = logging._levelColors
        except:
            colors = logging._levelColors = colormap
        
        # Set the logger's level.
        logging.Logger.__init__(self, name, level=level)

        # Disable the default propagation behavior, because yuck.
        self.propagate = propagate

        # Add any default handlers. By default this is the ColorHandler.
        for handler in handlers:
            self.addHandler(handler)

    @staticmethod
    def _getLevelNumbers():
        """ Returns the integer keys from the levelNames dictionary. """
        return [ik for ik in logging._levelNames.keys() if type(ik) is int]

    @staticmethod
    def _getLevelNames():
        """ Returns the string keys from the levelNames dictionary. """
        return [sk for sk in logging._levelNames.keys() if type(sk) is str]

    @staticmethod
    def addLevel(levelno, name, color):
        """ Adds a custom logging level with color. """
        logging._levelNames[levelno] = name
        logging._levelColors[levelno] = color

    @staticmethod
    def testmsgs(msg='test message'):
        """ Emit test messages for each defined logging level. """
        for level in ColorLogger._getLevelNumbers():
            logging.log(level=level, msg=msg)

if __name__ == '__main__':
    """ Example use. """

    # Set root logger class to use ColorLogger. ColorLogger uses
    # ColorStreamHandler & ColorFormatter by default (can be overridden).
    logging.root = ColorLogger('root')

    # Get ref to our root logger.
    logger = logging.getLogger()

    # Emit test messages.
    ColorLogger.testmsgs()

