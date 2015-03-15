__author__ = 'ashrith'

import socket
from multiprocessing import Process
import json

from model.node import Node


BUFFER_SIZE = 1024

class NodeGenerator(Node):
    def __init__(self, network_address):
        Node.__init__(self)
        self.network_address = network_address
        self.neighbor_map = {}
        self.socket = None
        self.listener = Process(target=self.listen)


    def listen(self):

        # find a port that is free for listening and bind my listener
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5000
        bind = False
        while not bind:
            try:
                self.socket.bind((self.ip, self.port))
                bind = True
                print("Client created on %s listening to port %s" % (self.ip, self.port))
            except socket.error:
                self.port += 1

        # tell my listening port and address to the network admin
        admin = socket.socket()
        admin.connect(self.network_address)
        admin.send(json.dumps({'type': 'intro', 'data': {'port': self.port, 'ip': self.ip}}))
        admin.close()
        while True:
            self.socket.listen(5)
            connection, address = self.socket.accept()
            self.process_message(connection.recv(BUFFER_SIZE))

    def process_message(self, msg):
        try:
            message = json.loads(msg)
            if message['type'] == 'admin_broadcast':
                data = message['data']
                print "BROADCAST: %s" % data

        except Exception:
            print 'Bad Message received'


    def stop(self):
        self.listener.terminate()

    def start(self):
        self.listener.run()




