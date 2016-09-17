#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify, request

import serial, socket

app = Flask(__name__)

# import the database and the tables from the database
from db import db
from db import Node, Sensor, Edge

nodes = Node.query.order_by(Node.label).all()
nodeList = []
for n in nodes:
	nodeList.append(n.label)	
# print nodeList[0]
print nodes

sensors = Sensor.query.order_by(Sensor.label).all()
sensorList = []
for s in sensors:
	sensorList.append(s.label)
# print sensorList[0]
print sensors

from commontools import log
import serial, time

#Setup listen socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8082              # Arbitrary non-privileged port
conn = None
adr = None
#Setup sending socket
#HOST = '0.0.0.0'    # The remote host
#PORT = 8083           # The same port as used by the server
#sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sender.connect((HOST, PORT))

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
			return render_template('standardMode.html')
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
			return render_template('standardMode.html')
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
		elif request.form['submit'] == 'Ping-Pong':
			print('\n')
			print '***************** Ping-Pong ******************'
			print('\n')
			print 'WRITE PING'
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			conn.sendall('PING')
			data = None
			while data != 'PONG':
				data = conn.recv(1024)
				if data == 'PONG':
					conn.close()
					return data
			print 'PING PONG'
			return render_template('standardMode.html')
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

