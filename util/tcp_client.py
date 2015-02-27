__author__ = 'admin'

import socket

''' client '''
import random
TCP_IP = '127.0.0.1'

TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(str(random.randint(0, 10)))
data = s.recv(BUFFER_SIZE)

s.close()

print "Server Reply:", data