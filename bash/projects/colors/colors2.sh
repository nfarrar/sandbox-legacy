#!/usr/bin/env bash


# iterm2 jellybeans:    http://goo.gl/PI2PGO
# lighten_colors.rb:    http://goo.gl/iy7yS8


# https://github.com/chriskempson/base16-shell

# Jellybeans {{{1
# ----------
# These are all variations on the 'jellybeans' colorscheme (one of my
# favorites). Using the iTerm2 jellybeans colorscheme, the vim-airline
# jellybeans colorscheme, the promptline.vim jellybeans colorcheme, and the
# tmuxline.vim jellybeans colorscheme results in completely inconsistent
# coloring between applications (shouldn't they all be the same!?).
# 
# - jellybeans.itermcolors                  http://git.io/CL8FVg
# - qtpi/Jellybeans.itermcolors             http://git.io/o2_PYQ
# - jellybeans.vim                          http://git.io/U_rg1w
# - bling/vim-airline - jellybeans.vim      http://git.io/aKrPxg
# - edkolev/promptline.vim - jelly.vim      http://git.io/n11BCA
# - edkolev/tmuxline.vim - jellybeans.vim   http://git.io/ilHW6g
# - itchyny/lightline - jellybeans.vim      http://git.io/2wXBMQ
#
# Unfortunately it's not that simple.
# - the iTerm2 jellybeans colorscheme defines only the base 16 xterm colors
#   0-15) and leaves the rest of the color space completely unmodified.
#
# - the iTerm2 jellybeans colorscheme uses truecolors defined in LSL, outside of
# the 8-bit colorspace.
#
# - vim (without experimental truecolor support) references with terminal colors
#   either by their xtername name or value
#   - we can still use the truecolors defined by in our xterm colorscheme
#     (0..15), however the rest of the colors are inconsistent and we have no
#     way to define colors using RGB
#   - furthermore, most of our syntax highlighting scripts and plugins will
#     display colors using the xterm palette, which again, will leave us with
#     very inconsistent coloring

# XTerm Colors {{{1
# ------------
#
# - XTerm supports 8-bit colors (defined by the values 0.255).
# - XTerm can actually support truecolor, but I haven't delved into this yet.
#
# - Colors 0..7 are the default terminal colors
# - Colors 8-15 are the bright terminal colors
# - Colors 16-231 (216 total) are the xterm-256 colors
# - Colors 232-255 are the xterm-256 monochrome colors
#
# Colors 16-231 are calculated by:
#
#   index = 16 + 36 * r + 6 * g + b (where r,g,b are in the range 0..5)
#
#
# Calculating XTerm-256 Colors: http://stackoverflow.com/q/27159322/212343
# http://permalink.gmane.org/gmane.comp.terminal-emulators.tmux.user/1324

# Base16 {{{1
# ------


# iTerm2 Jellybean Colors {{{1
# -----------------------
# This colorchart was contstructed from the iTerm2 jellybeans colorscheme. The
# colors are written as LSL values.

# RGB         Hex     Cterm
# ----------- ------- -----
# 226 115 115 #E27373 174
# 146 146 146 #929292 102
# 189 222 171 #BDDEAB 151
# 255 220 160 #FFDCA0 223
# 177 216 246 #B1D8F6 153
# 251 218 255 #FBDAFF 225
# 26  178 168 #1AB2A8 37
# 255 255 255 #FFFFFF 231
# 148 185 121 #94B979 108
# 255 185 123 #FFB97B 216
# 151 190 220 #97BEDC 110
# 225 192 250 #E1C0FA 183
# 0   142 142 #008E8E 30
# 222 222 222 #DEDEDE 188
# 189 189 189 #BDBDBD 145
# 255 161 161 #FFA1A1 217
# 18  18  18  #121212 N/A
# 255 255 255 #FFFFFF 231
# 255 165 96  #FFA560 215
# 255 255 255 #FFFFFF 231
# 222 222 222 #DEDE16 184
# 243 243 243 #DEDEDE 188
# 71  78  145 #474E91 60

# Name      RGB               Hex       256-Bit (Approximation)
# ----      ----------------  -------   -------
# Black     rgb(59,59,59)     #3b3b3b   59
# Red       rgb(207,106,76)   #cf6a4c   167
# Green     rgb(153,173,106)  #99ad6a   107
# Yellow    rgb(216,173,76)   #d8ad4c   179
# Blue      rgb(89,123,197)   #597bc5   68
# Magenta   rgb(160,55,176)   #a037b0   133
# Cyan      rgb(113,185,248)  #71b9f8   75
# White     rgb(173,173,173)  #adadad   145

# 236 - dark grey
# 239 - medium grey
# 244 - light grey
# 253 - bright grey
# 69  - blue
# 103 - purple
# 127 - magneta
# 150 - light green
# 173 - orange
# 196 - red
# 219 - light ink



