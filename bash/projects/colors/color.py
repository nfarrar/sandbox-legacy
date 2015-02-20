#! /usr/bin/env python

""" Color utilities for terminals.

# - websafe colors are encoded with only 6-bits (RRGGBB)
#   - each 
# - generates a 6x6x6 color cube
#

"""


__author__    = 'Nathan Farrar <nfarrar@crunk.io>'
__version__   = '0.1'
__copyright__ = 'Copyright (C) 2015 Nathan Farrar.  All rights reserved.'
__license__   = 'MIT'

import logging



def rgbtoxterm(r,g,b):
    number = 16 + 36 * r + 6 * g + b
    return number

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv == 1:
        v = int(value, 16)*17
        return v, v, v
    if lv == 3:
        return tuple(int(value[i:i+1], 16)*17 for i in range(0, 3))
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def test(number):

    # # r = (abs(number - 16) // 36) * 51
    # r = ((number - 16) // 36) * 51
    # g = (((number - 16) % 36) // 6) * 51
    # b = ((number - 16) % 6) * 51
    # return (r,g,b)

    index_R = ((number - 16) // 36)
    rgb_R = 55 + index_R * 40 if index_R > 0 else 0

    index_G = (((number - 16) % 36) // 6)
    rgb_G = 55 + index_G * 40 if index_G > 0 else 0

    index_B = ((number - 16) % 6)
    rgb_B = 55 + index_B * 40 if index_B > 0 else 0
    
    return (rgb_R, rgb_G, rgb_B)

print hex_to_rgb('#ff8787')
print test(0)
print rgbtoxterm(0,175,135)

if __name__ == '__main__':

