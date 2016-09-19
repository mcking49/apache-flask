"""
This file holds the database model. Each class represents an SQL table which
is automatically converted into SQL by the SQLAlchemy database package.
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Node Table
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True)
    d_type = db.Column(db.String(80))

    def __init__(self, label, d_type):
        self.label = label
        self.d_type = d_type

    def __repr__(self):
        return '<Device %r>' % self.label

# Edge Table
class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, device):
        self.device = device

    def __repr__(self):
        return '<Device %r>' % self.device
