#!/usr/bin/env python

# A very basic
import sys

try:
    import urwid
except ImportError as error:
    sys.stderr.write('Failed to import urwid: ' + str(error))
    sys.exit(1)


# color palette
palette = [
    ('titlebar', 'dark red', 'black'),
    ('body', 'white', 'default'),
    ('statusbar', 'white', 'dark blue')
]

# titlebar widget
titlebar = urwid.Text("titlebar")
titlebar = urwid.AttrWrap(titlebar, 'titlebar')

# body widget
body = urwid.Text('body')
body = urwid.Filler(body)
body = urwid.AttrWrap(body, 'body')

# statusbar widget
statusbar = urwid.Text('statusbar')
statusbar = urwid.AttrWrap(statusbar, 'statusbar')

# window widget
window = urwid.Frame(body,
                     header=titlebar,
                     footer=statusbar,
                     focus_part='footer')


def input(key):
    """handle input"""
    if key in ('Q', 'q', 'esc'):
        sys.exit(0)


if __name__ == '__main__':
    """main"""

    # event loop
    loop = urwid.MainLoop(window, palette, unhandled_input=input)
    loop.run()
