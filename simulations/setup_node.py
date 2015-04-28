__author__ = 'ashrith'

from lib.node_generator import NodeGenerator

network_ip = raw_input("Enter Network IP:")
if network_ip == "":
    network_ip = "127.0.0.1"
network_port = int(raw_input("Enter Network PORT:"))
print "Enter Location:"
loc_x = int(raw_input("x :"))
loc_y = int(raw_input("y :"))
node = NodeGenerator((network_ip, network_port), (loc_x,loc_y))

while True:
    print "[1] to start"
    print "[2] to stop"
    c = raw_input()
    if c == '1':
        node.start()
    if c == '2':
        node.stop()