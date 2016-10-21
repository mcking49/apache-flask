#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

import controller

from flask import Flask, make_response, render_template, jsonify, request
from db import Device
from commontools import log

app = Flask(__name__)
nodes = Device.query.filter_by(d_type='Node').order_by(Device.label).all()
sensors = Device.query.filter_by(d_type='Sensor').order_by(Device.label).all()

#Setup sockets
HOST = ''                 # Symbolic name meaning all available interfaces
SEND_PORT = 8082              # Arbitrary non-privileged
RECV_PORT = 8083
conn = None
adr = None

direction = "21"
speed = "50"
coordinator = controller.find_coordinater()

#-----------------------------------
@app.route('/', methods=['POST', 'GET'])
def index():
    """ Renders the index page.
    """
    return render_template('index.html')

#-----------------------------------
@app.route('/standardMode', methods=['POST', 'GET'])
def standardMode():
    """ Renders the Standard Mode Page.

    Performs any tasks that are required, then renders the Standard Mode page.
    """
    if request.method == 'POST':
        if request.form['submit'] == 'Speed':
            global speed
            speed = request.form['text']
            speed = speed.encode('ascii', 'ignore')
            controller.send_command(coordinator, speed, direction)
            print '================ {} ==============='.format(speed)
            return render_template('standardMode.html', nodes=nodes,
                                   sensors=sensors)
        elif request.form['submit'] == 'Forward':
            global direction
            direction = "21"
            controller.send_command(coordinator, speed, direction)
            print '================ {} ==============='.format(direction)
            return render_template('standardMode.html', nodes=nodes,
                                   sensors=sensors)
        elif request.form['submit'] == 'Backward':
            global direction
            direction = "20"
            controller.send_command(coordinator, speed, direction)
            print '================ {} ==============='.format(direction)
            return render_template('standardMode.html', nodes=nodes,
                                   sensors=sensors)
        elif request.form['submit'] == 'Start':
            controller.send_command(coordinator, speed, direction)
            return render_template('standardMode.html', nodes=nodes,
                                   sensors=sensors)
        elif request.form['submit'] == 'Stop':
            controller.send_command(coordinator, "0", direction)
            return render_template('standardMode.html', nodes=nodes,
                                   sensors=sensors)
    elif request.method == 'GET':
        return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors)


#-----------------------------------
@app.errorhandler(500)
def internal_error(error):
    """Error handler.
    """
    reply = []
    return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
    """Error handler.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)
