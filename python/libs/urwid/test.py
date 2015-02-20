#!/usr/bin/env python3


import urwid.curses_display
import urwid
import sys

title = urwid.Text(u"TITLEBAR")
status = urwid.Text(u"STATUSBAR")
body = urwid.Text(u"STATUSBAR")

base = urwid.Frame(title, body, status)


class UI(object):

    palette = [
        ('bg', 'light gray', 'dark blue'),
        ('fg', 'black', 'light gray', 'standout')
    ]

    def __init__(self):

        self.screen = urwid.curses_display.Screen()
        self.screen.register_palette(UI.palette)

        self.message = u"Hello World!"
        self.buffer = u""

        self.text = urwid.Text(self.message)
        self.fill = urwid.Filler(self.text, 'middle')

        self.screen.run_wrapper(self.run)

    def run(self):

        keys = None
        self.size = self.screen.get_cols_rows()

        while True:
            if keys:
                self.screen.draw_screen(self.size,
                                        self.fill.render(self.size, True))

            keys = self.screen.get_input()
            self.input(keys)

    def input(self, keys):
        self.messgage = self.message + str(keys)

        if "window resize" in keys:
            self.size = self.screen.get_cols_rows()

        elif "enter" in keys:
            self.text.set_text(self.buffer)
            self.buffer = u""

        elif 'esc' in keys:
            sys.exit(0)

        else:
            self.buffer = self.buffer + str(keys)


if __name__ == '__main__':
    ui = UI()
