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
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True)
    # status = db.Column(db.String(80))
    # location_x = db.Column(db.Integer)
    # location_y = db.Column(db.Integer)

    def __init__(self, label):
        self.label = label
        # self.status = status
        # self.location = [location_x, location_y]

    def __repr__(self):
        return '<Node %r>' % self.label

# Sensor Table
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True)
    # status = db.Column(db.String(80))
    # location_x = db.Column(db.Integer)
    # location_y = db.Column(db.Integer)

    def __init__(self, label):
        self.label = label
        # self.status = status
        # self.location = [location_x, location_y]

    def __repr__(self):
        return '<Sensor %r>' % self.label

# Edge Table
class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    node = db.relationship('Node', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, username):
        self.node = node

    def __repr__(self):
        return '<Node %r>' % self.node
