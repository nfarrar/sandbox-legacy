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


def titlebar_widget(text):
    """titlebar widget"""
    titlebar = urwid.Text(text)
    titlebar = urwid.AttrMap(titlebar, 'titlebar')
    return titlebar


def body_widget(text):
    """body widget"""
    body = urwid.Text(text)
    body = urwid.Filler(body)
    body = urwid.AttrMap(body, 'body')
    return body


def statusbar_widget(text):
    """statusbar widget"""
    statusbar = urwid.Text(text)
    statusbar = urwid.AttrMap(statusbar, 'statusbar')
    return statusbar


def window_widget(header, body, footer):
    """window widget"""
    window = urwid.Frame(body,
                         header=header,
                         footer=footer,
                         focus_part='footer')
    return window


def input(key):
    """handle input"""
    if key in ('Q', 'q', 'esc'):
        sys.exit(0)


if __name__ == '__main__':
    """main"""
    titlebar = titlebar_widget('titlebar')
    body = body_widget('body')
    statusbar = statusbar_widget('statusbar')

    window = window_widget(titlebar, body, statusbar)

    root = window

    # event loop
    loop = urwid.MainLoop(root, palette, unhandled_input=input)
    loop.run()
