"""
	:author: Miten Chauhan

    This file holds the functions required to send a command over the
    network to control a node. It also holds the function to identify which
    COM port the coordinator is plugged in to.
"""

import time
import serial
import serial.tools.list_ports

def send_command(com, speed, direction):
    """Send a command over the network.

    Sends a command over the network containing the nodes name to identify
    which node is the intended target, the direction that node should be
    travelling in, and the speed the node should be travelling at.

    Args:
        com: The COM port the coordinator is plugged in to. This is so the
            program knows which port to send the command through.
        speed: the speed the node should be travelling at.
        direction: the direction the node should be travelling in.
    """
    print '-------- STARTING --------'
    port = serial.Serial(com, baudrate=9600, timeout=0)
    node = 'BELLE'
    command = '~{}*{}*{}*#'.format(node, direction, speed)
    port.write(command)
    node_response = ''
    # time.sleep is set to 1 second to give the network enough time
    # to send the full message before reading it.
    time.sleep(1)
    node_response = port.readline()
    print node_response
    print '----------- FINISH -----------'

def find_coordinater():
    """Find the COM port for the coordinator.

    Identify the COM Port the coordinator is connected to by scanning through
    all the devices connected to com ports.

    Returns:
        The COM Port the coordinator is plugged in to, or 'unidentified' if
        the coordinator's COM port couldn't be found. A string is returned
        for example:

            'COM5'
    """
    com_port = 'unidentified'
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB Serial Port" in port[1]:
            com_port = port[0]
    print '====== COM PORT : {} ======'.format(com_port)
    return com_port
