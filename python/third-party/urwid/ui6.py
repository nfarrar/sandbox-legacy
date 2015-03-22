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

    def __init__(self):

        # append a 'test' element to the lines list
        self.lines = [
            urwid.Text('some text')
        ]

        # walker = urwid.SimpleListWalker(self.lines)
        self._w = urwid.ListBox(self.lines)

    def update(self, text):
        """create a new text widget and append it to the lines list"""

        self.lines.append(urwid.Text(text))


class Prompt(urwid.Edit):
    """prompt widget"""

    signals = ['update']

    def keypress(self, size, key):
        """process prompt input"""

        # quit on esc
        if key == 'esc':
            sys.exit(0)

        # normal behavior as the input is an enter
        elif key != 'enter':
            urwid.Edit.keypress(self, size, key)

        # when we press enter, clear the prompt and send a signal to
        # update the body widget text
        else:
            text = self.get_edit_text()
            self.set_edit_text('')
            urwid.emit_signal(self, 'update', text)
            return


class Window (urwid.Frame):
    """window widget"""

    pass


if __name__ == '__main__':
    """main"""

    titlebar = TitleBar('titlebar')
    body = Body()
    prompt = Prompt('> ')

    window = Window(body,
                    header=titlebar,
                    footer=prompt,
                    focus_part='footer')

    # create the event loop
    loop = urwid.MainLoop(
        window,
        palette,
        unhandled_input=input,
        handle_mouse=False
    )

    # signals

    # prompt the prompt box emits the signal from the keypress function
    # the signal calls body's update method
    urwid.connect_signal(prompt, 'update', body.update)

    # start the event loop
    loop.run()
