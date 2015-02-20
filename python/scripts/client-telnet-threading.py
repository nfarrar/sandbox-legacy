#!/usr/bin/env python

import collections
import socket
import threading

host = 'localhost'
port = 2000

input_buffer = collections.deque()
output_buffer = collections.deque()

class DisplayThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running == True:
            if len(output_buffer) > 0:
                data = output_buffer.pop()
                print data

    def die(self):
        self.running = False

class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.settimeout(1)
        self.skt.connect((host, port))
        self.running = True

    def run(self):
        while self.running == True:
            print '[ST] while loop'
            try:
                print '[ST] self.skt.recv() next'
                data = self.skt.recv(1024)
                output_buffer.append(data)
            except:
                print '[ST] except block'
                pass

            if len(input_buffer) > 0:
                print '[ST] trying to send data'
                try:
                    data = input_buffer.pop()
                    self.skt.send(data)
                except:
                    print '[ST] except, failed to send data'

        print '[ST] out of while loop'
        self.skt.close()

    def die(self):
        self.running = False

def main():
    print "[MAIN] Use 'quit' to exit client."

    sock_thread = SocketThread()
    sock_thread.start()

    display_thread = DisplayThread()
    display_thread.start()

    data = ''
    while data != 'quit':
        print '[MAIN] getting input: ',
        data = raw_input()
        input_buffer.append(data)

    sock_thread.die()
    display_thread.die()

if __name__ == '__main__':
    main()

