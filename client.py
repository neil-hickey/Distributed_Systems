import sys
from socket import socket
import urllib 

CRLF = "\r\n"
BUFFER_SIZE = 1024

# create a socket
sock = socket()
server_address = ('0.0.0.0', 8000)
sock.connect(server_address)

message = raw_input('Please enter your message to send: --> ')
encoded_message = urllib.quote(message)

request = [
    "GET /echo.php?message=%s HTTP/1.1" % encoded_message,
    "Host: localhost",
    "Connection: Close",
    "",
    "",
]

try:    
    # Send data
    print 'sending %s' % request
    sock.sendall(CRLF.join(request))

    # Get the response (in several parts, if necessary)
    response = ''
    buffer = sock.recv(BUFFER_SIZE)
    while buffer:
    	response += buffer
    	buffer = sock.recv(BUFFER_SIZE)

    # HTTP headers will be separated from the body by an empty line
    header_data, _, body = response.partition(CRLF + CRLF)

    print 'received %s' % body
except socket.error, (value, message):
	if sock:
		sock.close()
		print "Could not open socket:", message
		sys.exit(1)
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    sys.exit(1)