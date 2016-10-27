"""
	:author: Miten Chauhan

    This file holds the functions required to send a command over the
    network to control a node. It also holds the function to identify which
    COM port the coordinator is plugged in to.
"""

import time
import serial
import serial.tools.list_ports
import datetime

def emptyLog():
    """Deletes everything in the log file.

    Opens server_command_log.txt and overwrites everything inside the file
    with an empty string.
    """
    with open('server_command_log.txt', 'w') as log_file:
        log_file.write('')

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
    return com_port

def log_to_file(node, speed, direction, received):
    """Appends a string to a file.

    Saves a string to the end of the file.close

    Args:
        node: The name of the node the command was sent to.
        speed: the speed the node was set to.
        direction: the direction the node was set to.
        received: the message the node sent back to the server.    
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log = '{}\nSENT: node={}, speed={}, direction={}\nRECEIVED: {}\n \n'.format(current_time,node,speed,direction,received)
    with open('server_command_log.txt', 'a') as log_file:
        log_file.write(log)

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
    port = serial.Serial(com, baudrate=9600, timeout=0)
    node = 'BELLE'
    command = '~{}*{}*{}*#'.format(node, direction, speed)
    port.write(command)
    node_response = ''
    # time.sleep is set to 1 second to give the network enough time
    # to send the full message before reading it.
    time.sleep(1)
    node_response = port.readline()
    direction_name = ''
    if direction == '21':
        direction_name = 'Forward'
    else:
        direction_name = 'Backward'
    log_to_file(node, speed, direction_name, node_response)
