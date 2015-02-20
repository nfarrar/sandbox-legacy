#! /usr/bin/env python

# http://misc.flogisoft.com/bash/tip_colors_and_formatting
# https://github.com/chriskempson/base16-shell/blob/master/base16-chalk.dark.sh
# https://gist.github.com/MicahElliott/719710
# https://github.com/trapd00r/colorcoke

# http://stackoverflow.com/a/27165165/212343


# https://bbs.archlinux.org/viewtopic.php?pid=1179921#p1179921
# http://code.activestate.com/recipes/475116-using-terminfo-for-portable-color-output-cursor-co/
# https://github.com/broadinstitute/xtermcolor
# https://github.com/tartley/colorama
# https://github.com/dslackw/colored
# https://github.com/lepture/terminal
# https://github.com/erikrose/blessings

# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

# 
# https://web.njit.edu/~kevin/rgb.txt.html
# http://www.w3.org/TR/SVG/types.html#ColorKeywords

# https://superuser.com/questions/157563/programmatic-access-to-current-xterm-background-color

# http://linux.die.net/man/5/terminfo

def index_to_rgb(number):
    rgb_R = ((number - 16) // 36) * 51
    rgb_G = (((number - 16) % 36) // 6) * 51
    rgb_B = ((number - 16) % 6) * 51

    print '(', rgb_R, ", ", rgb_G, ", ", rgb_B, ")"

# index_to_rgb(17)


