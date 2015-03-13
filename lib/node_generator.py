__author__ = 'ashrith'

import socket
import logging
from multiprocessing import Process

from model.node import Node


class NodeGenerator(Node):
    def __init__(self):
        Node.__init__()
        self.neighbor_map = {}
        self.socket = None
        self.listener = None
        self.ip = '127.0.0.1'
        logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)
        self.listener = Process(target=self.listen)
        self.logger = logging.getLogger('serverLogger')


    @property
    def ip(self):
        return socket.gethostname()

    def broadcast(self, message):
        for address in self.nodes:
            self.socket.bind(address)

    def listen(self):
        self.socket.bind((self.ip, 5000))
        while True:
            self.socket.listen(5)
            connection, address = self.socket.accept()
            self.logger.info("New request to join Network (Address : %s )" % str(address))
            node = Node(address)
            self.nodes.append(node)
            print "New request to join Network (Address : %s )" % str(address)
            print "Total Nodes in Network = " + str(len(self.nodes))
            print self.nodes

    def stop(self):
        self.listener.terminate()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("Server created on %s listening to port %s" % (self.ip, 5000))
        self.listener.run()


# logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)



