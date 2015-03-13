__author__ = "ashrith"

import logging


class Node(object):
    def __init__(self, address):
        self.neighbors = []
        self.address = address

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
