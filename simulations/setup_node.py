__author__ = 'ashrith'

from lib.node_generator import NodeGenerator

network_ip = raw_input("Enter Network IP:")
network_port = int(raw_input("Enter Network PORT:"))

node = NodeGenerator((network_ip, network_port))

while True:
    print "[1] to start"
    print "[2] to stop"
    c = raw_input()
    if c == '1':
        node.start()
    if c == '2':
        node.stop()