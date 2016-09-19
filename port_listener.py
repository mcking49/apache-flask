import serial, socket, threading, Queue, time

class port_handler:

	# HOST = ''                 # Symbolic name meaning all available interfaces
	# SEND_PORT = 8082              # Arbitrary non-privileged port
	# RECV_PORT = 8083
	# send_conn = None
	# recv_conn = None
	# send_adr = None
	# recv_adr = None
	# command_queue = Queue.Queue()
	# r_command_queue = Queue.Queue()
	# connected = False

	# send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, host, send_port, recv_port):
		self.host = host
		self.send_port = send_port
		self.recv_port = recv_port
		self.send_conn = None
		self.recv_conn = None
		self.send_adr = None
		self.recv_adr = None
		self.command_queue = Queue.Queue()
		self.r_command_queue = Queue.Queue()
		self.connected = False

		self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def add_command(self, cmd):
		self.command_queue.put(cmd)

	def get_command(self):
		if not self.r_command_queue.empty():
			return self.r_command_queue.get()
		else:
			return None

	def listen(self, recv_conn):
		
		while recv_conn == None:
			self.recv_socket.bind((self.host, self.recv_port))
			self.recv_socket.listen(1)
			recv_conn, recv_adr = self.recv_socket.accept()
		print 'recv connected'
		recieved = None
		while(True):
			print 'loop listener'
			if not self.r_command_queue.empty():
				print self.r_command_queue.get()
			recieved = recv_conn.recv(1024)
			if recieved:
				self.r_command_queue.put(recieved)
			recieved = None

	def send(self, send_conn):
		while send_conn == None:
			self.send_socket.bind((self.host, self.send_port))
			self.send_socket.listen(1)
			send_conn, send_adr = self.send_socket.accept()
		print 'send connected'
		while True:
			print 'loop sender'
			cmd = self.command_queue.get(True)
			send_conn.sendall(cmd)

	def command_creator(self):
		count = 1
		while True :
			print 'loop creater'
			time.sleep(2)
			self.command_queue.put('Command : ' + str(count))
			count = count + 1


	def startListener(self):
		self.send_conn = None
		self.recv_conn = None
		# if not self.connected:
		# 	self.send_conn, self.recv_conn = self.connect(self.send_conn, self.recv_conn)
		listener = threading.Thread(target=self.listen, args = (self.recv_conn,))
		sender = threading.Thread(target=self.send, args = (self.send_conn,))
		# c = threading.Thread(target=self.command_creator)
		listener.daemon = True # setting daemon to true means threads wont stop program from closing
		sender.daemon = True
		# c.daemon = True
		listener.start()
		# c.start()
		sender.start()

	def connect(self, send_conn, recv_conn):
		while send_conn == None:
			self.send_socket.bind((self.host, self.send_port))
			self.send_socket.listen(1)
			send_conn, send_adr = self.send_socket.accept()
		while recv_conn == None:
			self.recv_socket.bind((self.host, self.recv_port))
			self.recv_socket.listen(1)
			recv_conn, recv_adr = self.recv_socket.accept()
		self.connected = True
		return send_conn, recv_conn