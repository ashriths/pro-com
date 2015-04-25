__author__ = 'ashishrawat'
import socket
from multiprocessing import Process

from demo_tracker import ColourTracker

colour_tracker = ColourTracker()
var1 = Process(target = colour_tracker.run())

print "first thread run"
var2 = Process(target = colour_tracker.run())

print "second thread run"
var3 = Process(target = colour_tracker.run())
print "third thread run"
