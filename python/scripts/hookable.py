#!/usr/bin/env python

"""

    Hookable provides dynamically bound, caching function hooks for
    asynchronous program environments.

    Hookable exposes two basic methods:
        register_hook(hook_id, function_reference)
        request_hook(hook_id) : return function_reference

    Interally hookable maintains a "network" of function hooks represented by
    collections of 'hookables'.  Hookable maintains an internal dictionary of
    hookables indexed by the 'hook_id' - only one hook_id can exist.  Users
    should be aware that hookable will not prevent rebinding of a hook id.

    Hookables cache function calls, the client can request a hook before that
    hook has been registered with a function reference.  At that time that the
    function reference is registered, the hookable will automatically process
    all cached function calls.

"""


from collections import deque

import logging

__author__ = "Nathan Farrar"
__email__ = "nathan.farrar@gmail.com"
__website__ = "http://0xsynack.net"
__source__ = "http://github.com/oxseyn"

__status__ = "Development"
__license__ = "GPL, v3.0"
__version__ = "0.1"


class Hookable:

    """
        A Hookable is a call-caching intermediate function reference.
        A Hookable can be created with an optional function reference, if no
        reference is provided then the function reference is set to None.
    """

    def __init__(self, function_reference=None):
        logging.debug('Hookable.__init__()')
        self._cache = deque()
        self._function_reference = function_reference

    def bind(self, function_reference):
        logging.debug('Hookable.bind()')
        self._function_reference = function_reference

    def execute(self, *args):
        if self._function_reference != None and len(self._cache) == 0:
            logging.debug('Hookable.execute(%s), if', str(args))
            exec('self._function_reference(' + ', '.join(map(str, args)) + ')')
        elif self._function_reference != None and len(self._cache) > 0:
            logging.debug('Hookable.execute(%s), elif', str(args))
            while len(self._cache) > 0:
                logging.debug('Hookable.execute(), while')
                exec('self._function_reference(' + ', '.join(map(str, self._cache.popleft())) + ')')
            exec('self._function_reference(' + ', '.join(map(str, args)) + ')')
        else:
            logging.debug('Hookable.execute(), else')
            self._cache.append(args)


class Hookables:

    """
    """

    def __init__(self):
        self._hookables = {}

    def register_hook(self, hook_id, function_reference):
        logging.debug('Hookables.register_hook()')
        if hook_id not in self._hookables.keys():
            self._hookables[hook_id] = Hookable(function_reference)
        else:
            self._hookables[hook_id].bind(function_reference)

    def request_hook(self, hook_id):
        logging.debug('Hookables.request_hook()')
        if hook_id not in self._hookables.keys():
            self._hookables[hook_id] = Hookable()
        return self._hookables[hook_id].execute


def register_hook(hook_id, function_reference):
    _hookables.register_hook(hook_id, function_reference)

def request_hook(hook_id):
    return _hookables.request_hook(hook_id)

_hookables = Hookables()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_func(*args):
        logging.info('test_func(%s)', str(args))

    t = request_hook('test_func')
    t(1)
    t(2)
    t(3)
    register_hook('test_func', test_func)
    t(4)
    t(5)
    t(6,7,8)


