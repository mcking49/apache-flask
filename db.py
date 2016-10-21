"""
    :author: Miten Chauhan

    This file holds the database model. Each class represents an SQL table which
    is automatically converted into SQL by the SQLAlchemy database package.
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Device(db.Model):
    """Table model for all Devices.

    This class represents the table model for all the devices.

    Attributes:
        id: an automatically generated id for a device.
        label: the name of the device.
        d_type: the type of the device (e.g. node or sensor)
    """
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True)
    d_type = db.Column(db.String(80))

    def __init__(self, label, d_type):
        """ Inits Device with relevant user info.
        """
        self.label = label
        self.d_type = d_type

    def __repr__(self):
        """A string representation of an item stored in the table.
        """
        return '<Device %r>' % self.label

# Edge Table
class Edge(db.Model):
    """Table model for an Edge.

    Attributes:
        id: an automaticallt generated id for an edge.
        Device_id: the id of the device the edge has a relationship with.
        device: the relationship between an Edge and a Device.
    """
    id = db.Column(db.Integer, primary_key=True)
    Device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, device):
        """Inits Edge with relevant user info.
        """
        self.device = device

    def __repr__(self):
        """A String representation of an edge.
        """
        return '<Device %r>' % self.device
