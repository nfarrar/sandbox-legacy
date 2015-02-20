#!/usr/bin/env python

import logging
import select
import socket


class Server:
    def __init__(self, address='0.0.0.0', port=51981, blocking=False):
        self._address = address
        self._port = port
        self._blocking = blocking
        self._socket = None

        self._connection = None
        self._remote_address = None

    def start(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setblocking(int(self._blocking))
            self._socket.bind((self._address, self._port))
            return True
        except socket.error, msg:
            self._socket = None
            logging.debug(msg)
            return False

    def listen(self):
        try:
            self._socket.listen(0)
            return True
        except socket.error, msg:
            self._socket = None
            logging.debug(msg)
            return False

    def send(self, data):
        try:
            self._socket.send(data)
            return True
        except socket.error, msg:
            self._socket = None
            logging.debug(msg)
            return False

    def close(self):
        try:
            self._socket.close()
            return True
        except socket.error, msg:
            self._socket = None
            logging.debug(msg)
            return False

    def accept(self):
        try:
            print self.skt.accept()
            print type(self.skt.accept())
        except:
            pass


def main():
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    server = Server()

    #(sread, swrite, sexc) =  select.select(readlist, [], [] );

if __name__ == '__main__':
    main()
