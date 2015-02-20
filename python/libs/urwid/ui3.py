#!/usr/bin/env python

import sys

try:
    import urwid
except ImportError as error:
    print >> sys.stderr, "Failed to import urwid: %s" % (error)
    sys.exit(1)


# color palette
palette = [
    ('titlebar', 'dark red', 'black'),
    ('body', 'white', 'default'),
    ('statusbar', 'white', 'dark blue')
]


class TitleBar (urwid.WidgetWrap):
    """titlebar widget"""

    def __init__(self, text):
        self._w = urwid.Text(text)
        self._w = urwid.AttrWrap(self._w, 'titlebar')


class Body (urwid.WidgetWrap):
    """body widget"""

    def __init__(self, text):
        self._w = urwid.Text(text)
        self._w = urwid.Filler(self._w)
        self._w = urwid.AttrWrap(self._w, 'body')


class StatusBar (urwid.WidgetWrap):
    """statusbar widget"""

    def __init__(self, text):
        self._w = urwid.Text(text)
        self._w = urwid.AttrWrap(self._w, 'statusbar')


class Window (urwid.Frame):
    """window widget"""

    pass


def input(key):
    """handle input"""
    if key == 'esc':
        sys.exit(0)


if __name__ == '__main__':
    """main"""

    titlebar = TitleBar('titlebar: press esc to quit')
    body = Body('body')
    statusbar = StatusBar('> ')

    window = Window(body, header=titlebar, footer=statusbar)

    root = window

    # event loop
    loop = urwid.MainLoop(root, palette, unhandled_input=input)
    loop.run()
