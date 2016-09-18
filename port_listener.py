import serial, socket, threading, Queue, time

HOST = ''                 # Symbolic name meaning all available interfaces
SEND_PORT = 8082              # Arbitrary non-privileged port
RECV_PORT = 8083
send_conn = None
recv_conn = None
send_adr = None
recv_adr = None
command_queue = Queue.Queue()
r_command_queue = Queue.Queue()
connected = False

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listen(recv_conn):
	recieved = None
	while(True):
		print 'loop listener'
		if not r_command_queue.empty():
			print r_command_queue.get()
		recieved = recv_conn.recv(1024)
		if recieved:
			r_command_queue.put(recieved)
		recieved = None

def send(send_conn):
	while True:
		print 'loop sender'
		cmd = command_queue.get(True)
		send_conn.sendall(cmd)

def command_creator():
	count = 1
	while True :
		print 'loop creater'
		time.sleep(2)
		command_queue.put('Command : ' + str(count))
		count = count + 1


def startListener():
	send_conn = None
	recv_conn = None
	if not connected:
		send_conn, recv_conn = connect(send_conn, recv_conn)
	listener = threading.Thread(target=listen, args = (recv_conn,))
	sender = threading.Thread(target=send, args = (send_conn,))
	c = threading.Thread(target=command_creator)
	listener.daemon = True
	sender.daemon = True
	c.daemon = True
	listener.start()
	c.start()
	sender.start()
	while(True):
		time.sleep(1)

def connect(send_conn, recv_conn):
	while send_conn == None:
		send_socket.bind((HOST, SEND_PORT))
		send_socket.listen(1)
		send_conn, send_adr = send_socket.accept()
	while recv_conn == None:
		recv_socket.bind((HOST, RECV_PORT))
		recv_socket.listen(1)
		recv_conn, recv_adr = recv_socket.accept()
	connected = True
	return send_conn, recv_conn

startListener()