__author__ = 'ashrith'

import socket
from multiprocessing import Process
import json

from model.node import Node


BUFFER_SIZE = 1024

class NetworkGenerator:
    def __init__(self):
        self.nodes = []
        self.neighbor_map = {}
        self.socket = None
        self.port = None
        self.listener = None
        self.ip = socket.gethostbyname('localhost')
        self.listener = Process(target=self.listen)

    def broadcast(self, message):
        for address in self.nodes:
            self.socket.bind(address)

    def listen(self):
        self.port = 5000
        bind = False
        while not bind:
            try:
                self.socket.bind((self.ip, self.port))
                bind = True
                print("Server created on %s listening to port %s" % (self.ip, self.port))
            except socket.error:
                self.port += 1
        while True:
            self.socket.listen(5)
            connection, add = self.socket.accept()
            self.process_message(connection.recv(BUFFER_SIZE))

    def process_message(self, msg):
        try:
            message = json.loads(msg)
            if message['type'] == 'intro':
                data = message['data']
                node = Node(ip=data['ip'], port=data['port'])
                self.nodes.append(node)
                print "New request to join Network (Address : %s )" % str(data)
                print "Total Nodes in Network = " + str(len(self.nodes))
                print self.nodes

        except Exception:
            print 'Bad Message received'


    def stop(self):
        self.listener.terminate()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.run()


# logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)


