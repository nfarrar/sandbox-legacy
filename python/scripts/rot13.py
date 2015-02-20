#!/usr/bin/env python

import optparse
import string
import sys

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-s", "--string", dest="input_string",
        help="parse an input string", metavar="INPUT_STRING")

    (options, args) = parser.parse_args()
    rot13 = string.maketrans( \
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", \
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    try:
        print string.translate(options.input_string, rot13)
    except:
        print string.translate('no input!', rot13)
