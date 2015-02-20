#!/usr/bin/env bash

# Bookmarks {{{1
#
# - http://re-factor.blogspot.com/2012/07/xterm-256color.html
# - https://superuser.com/questions/270214/how-can-i-change-the-colors-of-my-xterm-using-ansi-escape-sequences
# - http://www.steike.com/code/xterm-colors/
# - http://rtfm.etla.org/xterm/ctlseq.html
# - http://thrysoee.dk/xtermcontrol/
# - http://gidden.net/tom/2006/08/04/x11-color-list-for-macosx/
# - https://en.wikipedia.org/wiki/X11_color_names
# - https://codefodder.github.io/making-an-xterm-256color-chart/
# - https://unix.stackexchange.com/questions/118806/tmux-term-and-256-colours-support
# - https://unix.stackexchange.com/questions/23763/checking-how-many-colors-my-terminal-emulator-supports/23789#23789
# - http://www.tayloredmktg.com/rgb/
#
# Color Distance:
#
# - https://stackoverflow.com/questions/11765623/convert-hex-to-closest-x11-color-number
# - https://stackoverflow.com/questions/1313/followup-finding-an-accurate-distance-between-colors/74033#74033
#
# Blah: 
#
# - https://en.wikipedia.org/wiki/List_of_color_palettes
# - https://en.wikipedia.org/wiki/Color_depth
# - https://en.wikipedia.org/wiki/X11_color_names
# - https://en.wikipedia.org/wiki/SRGB
# - http://cgit.freedesktop.org/xorg/app/rgb/plain/rgb.txt
# - https://gist.github.com/XVilka/8346728
# - http://www.robmeerman.co.uk/unix/256colours#so_does_terminal_insert_name_here_do_256_colours
# - http://www.fifi.org/doc/xterm/xterm.faq.html
# - http://sixteencolors.net/
#
# - http://www.emanueleferonato.com/2009/08/28/color-differences-algorithm/
#
# - https://upload.wikimedia.org/wikipedia/en/1/15/Xterm_256color_chart.svg
# - http://www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
#
# - http://excess.org/misc/xterm_colour_chart.py.html
# }}}

# ESC[ … 38;2;<r>;<g>;<b> … m Select RGB foreground color
# ESC[ … 48;2;<r>;<g>;<b> … m Select RGB background color

# RGB
#
# - http://www.permadi.com/tutorial/websafecolor/
# - http://www.rapidtables.com/web/color/Web_Safe.htm
# - http://www.rapidtables.com/web/color/RGB_Color.htm
#
# Notes {{{1
#
# 8-Bit Colors
#
# - Using 8 bits (2^8) to store color information with the RGB model (RRGGBB),
#   we can define 256 (0.255) unique values.
# - Out of the 256 possible values, only 216 are mapped via the X11 rgb.txt.
#
# }}}

# Control Sequence Character {{{1
# --------------------------
# - http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
# - https://stackoverflow.com/questions/19062315/how-do-i-find-out-what-escape-sequence-my-terminal-needs-to-send
# - https://unix.stackexchange.com/questions/76566/where-do-i-find-a-list-of-terminal-key-codes-to-remap-shortcuts-in-bash

# export CSC=csc='\e'
# export CSC='\x1B'
export CSC='\033'

# Escape Bindings {{{1
export RESET="$CSC[0m"

export BOLD="$CSC[1m"
export DIM="$CSC[2m"
export UNDERLINE="$CSC[4m"
export BLINK="$CSC[5m"
export REVERSE="$CSC[7m"
export HIDDEN="$CSC[8m"

export BOLDOFF="$CSC[21m"
export DIMOFF="$CSC[22m"
export UNDERLINEOFF="$CSC[24m"
export BLINKOFF="$CSC[25m"

export FGBLACK="$CSC[30m"
export FGRED="$CSC[31m"
export FGGREEN="$CSC[32m"
export FGYELLOW="$CSC[33m"
export FGBLUE="$CSC[34m"
export FGMAGENTA="$CSC[35m"
export FGCYAN="$CSC[36m"
export FGLIGHTGRAY="$CSC[37m"
# [38m is used to define extended foreground colors
export FGDEFAULT="$CSC[39m"

export BGBLACK="$CSC[40m"
export BGRED="$CSC[41m"
export BGGREEN="$CSC[42m"
export BGYELLOW="$CSC[43m"
export BGBLUE="$CSC[44m"
export BGMAGENTA="$CSC[45m"
export BGCYAN="$CSC[46m"
export BGLIGHTGRAY="$CSC[47m"
# [48m is used to define extended background colors
export BGDEFAULT="$CSC[49m"

export FGDARKGRAY="$CSC[90m"
export FGLIGHTRED="$CSC[91m"
export FGLIGHTGREEN="$CSC[92m"
export FGLIGHTYELLOW="$CSC[93m"
export FGLIGHTBLUE="$CSC[94m"
export FGLIGHTMAGENTA="$CSC[95m"
export FGLIGHTCYAN="$CSC[96m"
export FGWHITE="$CSC[97m"

export BGDARKGRAY="$CSC[100m"
export BGLIGHTRED="$CSC[101m"
export BGLIGHTGREEN="$CSC[102m"
export BGLIGHTYELLOW="$CSC[103m"
export BGLIGHTBLUE="$CSC[104m"
export BGLIGHTMAGENTA="$CSC[105m"
export BGLIGHTCYAN="$CSC[106m"
export BGWHITE="$CSC[107m"

# }}}

# Make echo interpret escape sequences by default.
shopt -s xpg_echo



# Convert an rgb sequence ("RR,GG,BB") to the equivalent ascii escaped character
# sequence ("\e[38;2;00,00,00;m").
rgb_to_esc() {
  [[ $# -ne 1 ]] && return 64
  IFS=',' read -a rgb <<< "$1"
  echo -ne "$CSC[38;2;${rgb[0]};${rgb[1]};${rgb[2]};m"
}

hexrgb_to_esc() {
  [[ $# -ne 1 ]] && return 64
  echo -ne "\033]11;#53186f\007"
}

# Convert an rgb sequence ("RR,GG,BB") to the equivalent 'hexrgb' representation
# ("#3B3B3B").
rgb_to_hex() {
  [[ $# -ne 1 ]] && return 64
  IFS=',' read -a rgb <<< "$1"

  #local r=${rgb[0]} g=${rgb[1]} b=${rgb[2]}
  # color = (r*6/256)*36 + (g*6/256)*6 + (b*6/256)
  
  printf "#%02X%02X%02X" "${rgb[0]}" "${rgb[1]}" "${rgb[2]}"
}

h2d() {
  #printf "%d\n" "0x$1"
  echo $((16#${1}))
}

# Convert an rgb sequence ("RR,GG,BB") to the equivalent 'hexrgb' representation
rgb_to_xterm() {
  [[ $# -ne 1 ]] && return 64
  IFS=',' read -a rgb <<< "$1"
  local r=${rgb[0]} g=${rgb[1]} b=${rgb[2]}
  r=$(h2d $r); g=$(h2d $g); b=$(h2d $b)

  echo $(( 16 + (g * 36) + (g * 6) + b ))
  # echo $((16 + 36 * r + 6 * g + b ))
}

echo "$(rgb_to_xterm "0,0,0")"
echo "$(rgb_to_xterm "255,255,0")"


printcolor() {
  [[ $# -ne 2 ]] && return 64
  local name="$1" rgb="$2"
  local esc="$(rgb_to_esc "$2")"
  local hex="$(rgb_to_hex "$2")"

  # echo -e "$(rgbesc "$2")$(rgbtohex "$2")\t\t${2}\t${1}$(clear)"
  echo "$esc$name\t\t$rgb\t$hex"
}

echo 'jellybeans.vim'
printcolor 'black'    '59,59,59' 
printcolor 'red'      '207,106,76'
printcolor 'green'    '153,173,106'
printcolor 'yellow'   '216,173,76'
printcolor 'blue'     '89,123,197'
printcolor 'magenta'  '160,55,176'
printcolor 'cyan'     '113,185,248'
printcolor 'white'    '173,173,173'




# vim set: ft=sh fdm=marker
