#!/usr/bin/env python

import logging
import optparse
import select
import socket

ports=range(1,65526)

class Service:
  def __init__(self, port):
    self.skt = None       # listening socket object
    self.port = port      # port socket is listening on for incoming connections
    self.skts = []        # list containing negotiated child sockets

  def start(self):
    try:
      self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.skt.setblocking(0)
      self.skt.bind(('0.0.0.0',self.port))
      self.skt.listen(0)
      return True
    except socket.error, msg:
      print msg
      self.skt = None
      self.port = None
      return False

  def close(self):
    for s in self.sockets:
      s.close()
    self.s.close

  def accept(self):
    try:
      print self.skt.accept()
      print type(self.skt.accept())
    except:
      pass

def main():
  s = Service(1025)
  s.start()
  while True:
    s.accept()
    #(sread, swrite, sexc) =  select.select(readlist, [], [] );

if __name__ == '__main__':
  main()

