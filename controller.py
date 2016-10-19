import serial
import serial.tools.list_ports
import time

"""
Send a command over the network.
"""
def start(com, speed, direction):
    print '-------- STARTING --------'
    port = serial.Serial(com, baudrate=9600, timeout=0)
    node = 'BELLE'
    port.write('~' + node + '*' + direction + '*' + speed + '*' + '#')
    data = ''
    # time.sleep is set to 1 second to give the network enough time
    # to send the full message before reading it.
    time.sleep(1)
    data = port.readline()
    print(data)
    print '----------- FINISH -----------'

"""
Stops a node from moving.
"""
def stop(com, speed, direction):
    print '-------- STOPPING --------'
    port = serial.Serial(com, baudrate=9600, timeout=0)
    node = 'BELLE'
    port.write('~' + node + '*' + direction + '*' + speed + '*' + '#')
    data = ''
    # time.sleep is set to 1 second to give the network enough time
    # to send the full message before reading it.
    time.sleep(1)
    data = port.readline()
    print(data)
    print '----------- FINISH -----------'


"""
Identify the COM port the coordinator node is connected to.
"""
def find_coordinater():
    com_port = 'unidentified'
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "USB Serial Port" in p[1]:
            com_port = p[0]
        print('===== COM Port: ' + com_port)
    return com_port