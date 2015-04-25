__author__ = 'ashrith'

import socket
from multiprocessing import Process
from threading import Thread
import json

from model.node import Node


BUFFER_SIZE = 1024

class NetworkGenerator(Thread):
    def __init__(self):
        Thread.__init__(self);
        self.nodes = []
        self.sentinel = False
        self.neighbor_map = {}
        self.socket = None
        self.port = None

        self.ip = '127.0.0.1'
        #self.listener = Process(target=self.listen)
    '''
    def get_host_ip(self):
        self.ip = socket.gethostbyname(socket.gethostname())
    '''
    #var =  socket.gethostbyname(socket.gethostname())

    def run(self):
        self.listen()

    def broadcast(self, message):
        for node in self.nodes:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((node.ip, node.port))
            s.send(message)
            s.close()

    def listen(self):
        self.port = 5000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bind = False
        self.sentinel = True
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
        # try:
        message = json.loads(msg)
        if message['type'] == 'intro':
            data = message['data']
            node = Node(ip=data['ip'], port=data['port'])
            self.nodes.append(node)
            self.broadcast(json.dumps(
                {'type': 'admin_broadcast', 'from': 'admin', 'data': "New Node in Network, Address : %s" % str(data)}))
            print "New request to join Network (Addr1ess : %s )" % str(data)
            print "Total Nodes in Network = " + str(len(self.nodes))
            print self.nodes


    def stop(self):
            self.run = False
            print "Server Stopped"
    # def start(self):
    #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.listener.run()


# logging.basicConfig(filename='server.log', filemode='w', level=logging.DEBUG)


