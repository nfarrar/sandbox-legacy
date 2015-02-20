#!/usr/bin/env python

from optparse import OptionParser
from twisted.conch.telnet import Telnet
from twisted.internet import stdio
from twisted.internet.protocol import ClientFactory
from twisted.protocols import basic
from twisted.python import log

import termios, sys

logFile = "log-twistedclient.log"

class TelnetClient(Telnet):
    factory = None
    connected = False

    def connectionMade(self):
        log.msg('TelnetClient.connectionMade()')
        self.connected = True

    def applicationDataReceived(self, data):
        log.msg('TelnetClient.applicationDataReceived(): ' + data)
        self.factory.console.writeData(data)

    def connectionLost(self, reason):
        log.msg('TelnetClient.connectionLost()')

    def enableRemote(self, option):
        log.msg('TelnetClient.enableRemote(): ' + option)
        self.factory.console.disableLocalEcho()
        return True

    def disableRemote(self, option):
        log.msg('TelnetClient.disableRemote(): ' + option)
        self.factory.console.enableLocalEcho()
        return True

    def writeData(self, data):
        log.msg('TelnetClient.sendData(): ' + data)
        self.transport.write(data)

class TelnetClientFactory(ClientFactory):
    reactor = None
    client = None

    def buildProtocol(self, address):
        log.msg('TelnetClientFactory.buildProtocol()')
        self.client = TelnetClient()
        self.client.factory = self
        return self.client

    def startedConnecting(self, connector):
        log.msg('TelnetClientFactory.startedConnecting()')

    def clientConnectionFailed(self, connector, reason):
        log.msg('TelnetClientFactory.clientConnectionFailed()')
        print 'connection was refused.'
        self.reactor.stop()

    def clientConnectionLost(self, connector, reason):
        log.msg('TelnetClientFactory.clientConnectionLost')
        self.reactor.stop()

class Console(basic.LineReceiver):
    from os import linesep as delimiter
    factory = None
    consoleFD = None
    TTYEnabled = None
    TTYDisabled = None

    def connectionMade(self):
        self.consoleFD = sys.stdin.fileno()
        self.TTYEnabled = termios.tcgetattr(self.consoleFD)
        self.TTYDisabled = termios.tcgetattr(self.consoleFD)
        self.TTYDisabled[3] = self.TTYDisabled[3] & ~termios.ECHO

    def lineReceived(self, line):
        log.msg('Console.lineReceived()')
        self.factory.client.writeData(line + '\r\n')

    def writeData(self, data):
        log.msg('Console.writeData()')
        self.transport.write(data)

#    def disableLocalEcho(self):
#        try:
#            termios.tcsetattr(self.consoleFD, termios.TCSADRAIN, self.TTYDisabled)
#        except:
#            log.msg('Console.disableLocalEcho(): failed')

#    def enableLocalEcho(self):
#        try:
#            termios.tcsetattr(self.consoleFD, termios.TCSADRAIN, self.TTYEnabled)
#        except:
#            log.msg('Console.enableLocalEcho(): failed')

def main():

    usage = 'python twistedclient.py -a address -p port'
    parser = OptionParser(usage=usage)
    parser.add_option('-a', '--address', dest='address', default='localhost')
    parser.add_option('-p', '--port', dest='port', default=23)
    (options, args) = parser.parse_args()

    log.startLogging(open(logFile, 'w'), setStdout=False)
    console = Console()
    factory = TelnetClientFactory()

    console.factory = factory
    factory.console = console

    stdio.StandardIO(console)

    from twisted.internet import reactor
    reactor.connectTCP(options.address, int(options.port), factory)
    factory.reactor = reactor
    reactor.run()

if __name__ == '__main__':
    main()

