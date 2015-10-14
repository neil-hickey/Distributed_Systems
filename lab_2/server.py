import select, socket
from threadpool import *

class Server():
	def __init__(self, host, port, workers=20):
		self.pool = ThreadPool(workers)
		self.host = host
		self.port = port

	def start(self):
		self.stop_server = False
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.sock.listen(8)
		print "Starting server... \nListening on %s:%d" % (self.host, self.port)

		while not self.stop_server:
			try:
				read_sockets, _, _ = select.select([self.sock],[],[])
				for sock in read_sockets:
					if sock is self.sock:
						conn, addr = sock.accept()
						print 'Incoming connection from %s' % (repr(addr))
						try:
							self.pool.submit(self.worker(conn, addr))
						except Queue.full:
							conn.sendall("Service unavailable\n")
							conn.close()
			except select.error:
				self.stop_server = True
				

	def worker(self, conn, addr):
		 # try reading data from the socket
		msg = ''
		try:
			data = conn.recv(1024)
			msg += data
		except socket.error, e:
			print "socket error ", e

		# check data for our commands
		if msg == "KILL_SERVICE\n":
			Thread(target=self.shutdown, args=[False]).start()
		elif msg[:4] == 'HELO':
			print "sending..." 
			print "%sIP:%s\nPort:%s\nStudentID:12306113" % (msg,  socket.gethostbyname(socket.gethostname()), addr[1])
			conn.sendall("HELO %sIP:%s\nPort:%s\nStudentID:12306113" % (msg,  socket.gethostbyname(socket.gethostname()), addr[1]))
		else:
			print "Unrecognized Command"
			conn.sendall("Unrecognized Command")

		# Kill the connection
		conn.close()

	def shutdown(self, safe=True):
		self.stop_server = True
		if safe and self.pool is not None:
			self.pool.shutdown()
		self.sock.close()
