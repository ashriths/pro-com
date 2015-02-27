__author__ = 'ashrith'

import socket
import logging


class NetworkGenerator:
    def __init__(self):
        self.nodes = []
        self.neighbor_map = {}
        self.socket = None
        self.listener = None
        logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)
        self.logger = logging.getLogger('serverLogger')
        ##self.logger.setConsoleLevel(logging.INFO)

    @property
    def ip(self):
        return socket.gethostname()

    def broadcast(self, msg):
        for node in self.nodes:
            self.socket.bind(node):
            
            print str(node)

    def listen(self):
        while True:
            connection, address = self.socket.accept()
            self.logger.info("New request to join Network (Address : %s )" % str(address))
            self.nodes.append(address)
            name = connection.recv(1024)
            print "New request to join Network (name : %s , Address : %s )" % (name, str(address))
            connection.send("The server has accepted you request. ")
            self.broadcast("New Node in network called "+name)
            self.socket.bind((self.ip, port))
            self.socket.listen(5)


    def start(self, port=5000):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.logger.info("Server created on %s listening to port %s" % (self.ip, port))
        self.socket.listen(5)
        self.listen()


# logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)
gen = NetworkGenerator()
gen.start()

