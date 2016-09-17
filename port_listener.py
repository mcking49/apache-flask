import serial, socket, threading, Queue

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8082              # Arbitrary non-privileged port
conn = "Unchanged"
adr = None
command_queue = Queue.Queue()
r_command_queue = Queue.Queue()
connected = False

serial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listener():
	while(True):
		if not command_queue.empty():
			cmd = command_queue.get()
			conn.sendAll(cmd)
		recieved = serial_socket.recv(1024)
		if recieved:
			r_command_queue.put(recieved)

def startListener():
	if not connected:
		connect()
	t = threading.Thread(target=listener())
	t.daemon = True
	t.start()

def connect():
	while not conn:
		serial_socket.bind((HOST, PORT))
		serial_socket.listen(1)
		conn, adr = serial_socket.accept()
	connected = True