#!/usr/bin/env python3

import logging


class BaseClass (object):
    def __init__(self):
        logging.debug('BaseClass.__init__()')


class ChildClassA (BaseClass):
    def __init__(self):
        logging.debug('ChildClassA.__init__()')


class ChildClassB (BaseClass):
    def __init__(self):
        logging.debug('ChildClassB.__init__() : super(ChildClassB, self).__init__()')
        super(ChildClassB, self).__init__()


class ChildClassC (BaseClass):
    def __init__(self):
        logging.debug('ChildClassC.__init__() : super(BaseClass, self).__init__()')
        super(BaseClass, self).__init__()


class ChildClassD (BaseClass):
    def __init__(self):
        logging.debug('ChildClassD.__init__() : super().__init__()')
        super().__init__()


if __name__ == '__main__':

    log_format = "[%(filename)s : %(lineno)3s ] %(message)s "
    log_level = logging.DEBUG

    logging.basicConfig(level=logging.DEBUG, format=log_format)

    base = BaseClass()
    childa = ChildClassA()
    childb = ChildClassB()
    childc = ChildClassC()
    childd = ChildClassD()
