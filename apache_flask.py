#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify, request

import serial, socket, port_listener

app = Flask(__name__)

# import the database and the tables from the database
from db import db
from db import Device, Edge

nodes = Device.query.filter_by(d_type='Node').order_by(Device.label).all()
sensors = Device.query.filter_by(d_type='Sensor').order_by(Device.label).all()

from commontools import log
import serial, time, port_listener

#Setup sockets
HOST = ''                 # Symbolic name meaning all available interfaces
SEND_PORT = 8082              # Arbitrary non-privileged 
RECV_PORT = 8083
conn = None
adr = None

port_handler = port_listener.port_handler(HOST, SEND_PORT, RECV_PORT)
port_handler.startListener()

def sendMsg(msg):
	port_handler.add_command(msg)

def pollMsg():
	cmd = port_handler.get_command()
	if cmd:
		print cmd
	else:
		print 'No Command'
	return cmd
	

#-----------------------------------
@app.route('/', methods=['POST', 'GET'])
def index():    
	return render_template('index.html')
	
#-----------------------------------
@app.route('/standardMode', methods=['POST', 'GET'])
def standardMode():
	if request.method == 'POST':
		if request.form['submit'] == 'Setup':
			print('\n')
			print '***************** SETUP ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			while not conn:
				conn, adr = s.accept()
			#sender.sendall('PING')
			return render_template('standardMode.html', nodes=nodes, sensors=sensors)
		if request.form['submit'] == 'Ping':
			print('\n')
			print '***************** PINGING ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			conn.sendall('PING')
			conn.recv(1024)
			#sender.sendall('PING')
			conn.close()
			return render_template('standardMode.html', nodes=nodes, sensors=sensors)
		elif request.form['submit'] == 'Pong':
			print('\n')
			print '***************** WAITING FOR DATA ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			while True :
				data = conn.recv(1024)
				if data:
					return data
		if request.form['command'] == 'Activate Node':
			sendMsg('Activate Node: ' + request.form['node'])
			return render_template('index.html')
		elif request.form['command'] == 'Deactivate Node':
			sendMsg('Deactivate Node: ' + request.form['node'])
			return render_template('index.html')
		elif request.form['submit'] == 'Ping-Pong':
			print('\n')
			print '***************** Ping-Pong ******************'
			print('\n')
			print 'WRITE PING'
			sendMsg('PING')
			msg = pollMsg()
			print 'PING PONG'
			return render_template('standardMode.html', nodes=nodes, sensors=sensors)
	elif request.method == 'GET':
		return render_template('standardMode.html', nodes=nodes, sensors=sensors)


#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

