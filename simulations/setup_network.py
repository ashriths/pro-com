__author__ = 'ashrith'

from lib.network_generator import NetworkGenerator
from threading import Thread

gen = NetworkGenerator()
while True:
    print "[1] to start"
    print "[2] to stop"
    c = raw_input()
    if c == '1':
        gen.start()
    if c == '2':
        gen.stop();