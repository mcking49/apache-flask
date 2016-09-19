import serial, socket, threading, Queue, time

class PortHandler:
	"""A serial port / socker handler.

	PortHandler handles the serial ports and sockets required to send
	information in the form of commands, through the network.
	"""

	
	def __init__(self, host, send_port, recv_port):
		"""Inits PortHandler"""
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
		"""Add a command to the queue.

		Args:
			cmd: the command to be added to the queue
		"""
		self.command_queue.put(cmd)

	def get_command(self):
		"""Gets received command.

		Returns:
			None
		"""
		if not self.r_command_queue.empty():
			return self.r_command_queue.get()
		else:
			return None

	def listen(self, recv_conn):
		"""Listener that adds received commands to the queue.

		A listener that connects to the recv port and adds received commands to
		the queue.

		Args:
			recv_conn: 		
		"""
		#Connect to socket
		while recv_conn == None:
			self.recv_socket.bind((self.host, self.recv_port))
			self.recv_socket.listen(1)
			recv_conn, recv_adr = self.recv_socket.accept()
		print 'recv connected'
		#Listen to socket
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
		"""Send commands.

		Connects to the send port and sends commands via the send port.

		Args:
			send_conn:
		"""
		#Connect to port
		while send_conn == None:
			self.send_socket.bind((self.host, self.send_port))
			self.send_socket.listen(1)
			send_conn, send_adr = self.send_socket.accept()
		print 'send connected'
		#Send comands from queue
		while True:
			print 'loop sender'
			cmd = self.command_queue.get(True)
			send_conn.sendall(cmd)

	def startListener(self):
		"""Start threads.

		Starts the threads for receiving commands and for sending commands.
		"""
		self.send_conn = None
		self.recv_conn = None
		listener = threading.Thread(target=self.listen, args = (self.recv_conn,))
		sender = threading.Thread(target=self.send, args = (self.send_conn,))
		listener.daemon = True # setting daemon to true means threads wont stop program from closing
		sender.daemon = True
		listener.start()
		sender.start()