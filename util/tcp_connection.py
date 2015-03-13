__author__ = 'admin'

import logging
import socket

BUFFER_SIZE = 1024


class TCPException(Exception):
    pass


class TCPConnection(object):
    def __init__(self, ip='127.0.0.1', port=5001):
        """
        :rtype : object
        :type ip: str
        :type port: int
        :arg ip: ip address of the host
        :arg port: port number of the host
        """
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('TCPConnection : Socket created')

    def send(self, message):
        if self.socket is None:
            logging.exception('Socket creation unsuccessful')
            raise TCPException('Socket connection was not established')
        try:
            self.socket.connect((self.ip, self.port))
            self.socket.send(message)
            reply = self.socket.recv(BUFFER_SIZE)
            return reply
        except socket.error as e:
            raise TCPException('Cannot connect to Server %s:%s' % (self.ip, self.port))


s = TCPConnection()



