#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

import controller
import os

from flask import Flask, make_response, render_template, jsonify, request
from werkzeug.utils import secure_filename
from db import Device
from commontools import log

UPLOAD_FOLDER = 'static/images/floorplans'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

nodes = Device.query.filter_by(d_type='Node').order_by(Device.label).all()
sensors = Device.query.filter_by(d_type='Sensor').order_by(Device.label).all()

#Setup sockets
HOST = ''                 # Symbolic name meaning all available interfaces
SEND_PORT = 8082              # Arbitrary non-privileged
RECV_PORT = 8083
conn = None
adr = None

# initially loads blank canvas for visJS diagram
filename = ''

# Default device variables
direction = '21'
speed = '10'
node = 'BELLE'
coordinator = controller.find_coordinater()

# Default disabled buttons on standardMode.html
# start = ''
# stop = 'disabled'
# forward = 'disabled'
# backward = ''

#-----------------------------------
@app.route('/', methods=['POST', 'GET'])
def index():
    """ Renders the index page."""
    return render_template('index.html')

#-----------------------------------
@app.route('/standardMode', methods=['POST', 'GET'])
def standardMode():
    """ Renders the Standard Mode Page.

    Performs any tasks that are required, then renders the Standard Mode page.
    """
    if request.method == 'POST':
        if request.form['submit'] == 'Node':
            global node
            node = request.form['node'].upper()
            print '\n\n\n================ {} ===============\n\n\n'.format(node)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Set speed of node
        elif request.form['submit'] == 'Speed':
            global speed
            speed = request.form['speed']
            speed = speed.encode('ascii', 'ignore')
            controller.send_command(coordinator, speed, direction, node)
            print '================ {} ==============='.format(speed)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Make node go forward
        elif request.form['submit'] == 'Forward':
            global direction
            direction = "21"
            global forward
            forward = 'disabled'
            global backward
            backward = ''
            controller.send_command(coordinator, speed, direction, node)
            print '================ {} ==============='.format(direction)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Make node go backward
        elif request.form['submit'] == 'Backward':
            global direction
            direction = "20"
            global forward
            forward = ''
            global backward
            backward = 'disabled'
            controller.send_command(coordinator, speed, direction, node)
            print '================ {} ==============='.format(direction)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Start node
        elif request.form['submit'] == 'Start':
            global start
            start = 'disabled'
            global stop
            stop = ''
            # controller.test()
            controller.send_command(coordinator, speed, direction, node)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Stop node
        elif request.form['submit'] == 'Stop':
            global start
            start = ''
            global stop
            stop = 'disabled'
            controller.send_command(coordinator, "0", direction, node)
            return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)
        # Set Floor Plan
        elif request.form['submit'] == 'Set Floor Plan':
            file = request.files['file']
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('standardMode.html', nodes=nodes,
                            sensors=sensors, filename=filename,
                            speed=speed, node=node)
        elif request.form['submit'] == 'Empty Log File':
            controller.emptyLog()
            return render_template('standardMode.html', nodes=nodes,
                            sensors=sensors, filename=filename,
                            speed=speed)
    elif request.method == 'GET':
        return render_template('standardMode.html', nodes=nodes,
                               sensors=sensors, filename=filename,
                               speed=speed, node=node)


#-----------------------------------
@app.errorhandler(500)
def internal_error(error):
    """Error handler."""
    reply = []
    return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
    """Error handler."""
    return make_response(jsonify({'error': 'Not found'}), 404)
