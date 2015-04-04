__author__ = "ashrith"

import logging
import socket

class Node(object):
    def __init__(self, ip='192.168.43.124', port=5000):
        self.neighbors = []
        self.ip = ip
        self.port = port

    def get_host_ip(self):
        self.ip = socket.gethostbyname(socket.gethostname())

    def add_neighbor(self, node):
        """
        :param node: node to be added to the neighbors list
        :type node: Node
        :return: None
        :rtype: None
        """
        if isinstance(node, Node):
            self.neighbors.append(node)
        else:
            logging.error('Node.add_neighbor : tried to push non node into network')

