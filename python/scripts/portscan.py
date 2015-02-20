#!/usr/bin/env python

import socket
import sys
import threading
import optparse
import IPy

MAX_THREADS = 50

class Scanner(threading.Thread):
    def __init__(self, address="127.0.0.1", netmask="255.255.255.255", start="1", end="1024"):
        threading.Thread.__init__(self)
        self.address = address
        self.netmask = netmask
        self.start = start
        self.end = end

    def scan_host(self, address, start="1", end="1024"):
        for x in range(int(start), int(end)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((address, x))
                print "%s:%d OPEN" % (address, x)
                s.close()
            except:
                pass

    def scan_network(self, address="127.0.0.1", netmask="255.255.255.255", start="1", end="1024"):
        pass 

def main():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--address", dest="address", default="127.0.0.1")
    parser.add_option("-n", "--netmask", dest="netmask", default="255.255.255.255")
    parser.add_option("-s", "--start", dest="start", default="1")
    parser.add_option("-e", "--end", dest="end", default="1024")
    (options, args) = parser.parse_args()

    scanner = Scanner(options.address, options.netmask, options.start, options.end)

if __name__ == "__main__":
    main()

