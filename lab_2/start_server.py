import sys, socket
from server import *

def start_server():
    # Start the server 
    s = Server('0.0.0.0', int(sys.argv[1]))
    s.start()

if __name__ == '__main__':
    start_server()