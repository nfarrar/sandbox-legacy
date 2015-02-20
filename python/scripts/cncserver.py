#!/usr/bin/env python

"""
    example server              http://as.ynchrono.us/2011/03/twisted-conch-in-60-seconds.html
    key auth example            https://github.com/dreamhost/dreamssh/

    twisted.conch.ssh.agent ???
    twisted.conch.ssh.agent.messages.items()

    twisted.internet.protocol.Protocol -> makeConnection uses transport
    transport is in twisted.conch.ssh.session.SSHSessionProcessProtocol ***
"""

from twisted.internet.protocol import Protocol
from twisted.cred.portal import Portal
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.conch.interfaces import IConchUser
from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.session import SSHSession, SSHSessionProcessProtocol, wrapProtocol
from twisted.cred.checkers import FilePasswordDB
from twisted.python.filepath import FilePath
from twisted.python import log
import base64
import binascii
import sys


with open('server_keys/id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey = Key.fromString(data=privateBlob)

with open('server_keys/id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey = Key.fromString(data=publicBlob)

class PublicKeyDatabase(SSHPublicKeyDatabase):
    def getAuthorizedKeysFiles(self, credentials):
        #if config.ssh.usesystemkeys:
        #    return SSHPublicKeyDatabase.getAuthorizedKeysFiles(
        #        self, credentials)
        #return [FilePath(config.ssh.userauthkeys.replace("{{USER}}", credentials.username))]
        return FilePath('server_keys')

    def checkKey(self, credentials):
        #
        #if config.ssh.usesystemkeys:
        #    return SSHPublicKeyDatabase.checkKey(
        #        self, credentials)
        #for filePath in self.getAuthorizedKeysFiles(credentials):
        #    if not filePath.exists():
        #        continue
        #    lines = filePath.open()
        #    for line in lines:
        #        lineData = line.split()
        #        if len(lineData) < 2:
        #            continue
        #        try:
        #            if base64.decodestring(lineData[1]) == credentials.blob:
        #                return True
        #        except binascii.Error:
        #            continue
        #return False
        return True

class EchoProtocol(Protocol):
    def connectionMade(self):
        #self.transport.write("Echo protocol connected\r\n")
        log.msg('echo protocol connected')

    def dataReceived(self, bytes):
        #self.transport.write("echo: " + repr(bytes) + "\r\n")
        log.msg(repr(bytes))

    def connectionLost(self, reason):
        print 'Connection lost', reason

def nothing():
    pass

class SimpleSession(SSHSession):
    name = 'session'

    def request_pty_req(self, data):
        return True

    def request_shell(self, data):
        log.msg(data)
        protocol = EchoProtocol()
        transport = SSHSessionProcessProtocol(self)
        protocol.makeConnection(transport)
        transport.makeConnection(wrapProtocol(protocol))
        self.client = transport
        return True

class SimpleRealm(object):
    def requestAvatar(self, avatarId, mind, *interfaces):
        user = ConchUser()
        user.channelLookup['session'] = SimpleSession
        log.msg(user)
        return IConchUser, user, nothing

def main():
    log.startLogging(sys.stdout)

    factory = SSHFactory()
    factory.privateKeys = {'ssh-rsa': privateKey}
    factory.publicKeys = {'ssh-rsa': publicKey}
    factory.portal = Portal(SimpleRealm())
    #factory.portal.registerChecker(FilePasswordDB("ssh-passwords"))
    factory.portal.registerChecker(SSHPublicKeyDatabase())

    from twisted.internet import reactor
    reactor.listenTCP(2022, factory)
    reactor.run()

if __name__ == '__main__':
    main()
