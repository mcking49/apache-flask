"""
    This file holds the script to make a database using the model in db.py

    Before running this file note the following:
        - If there is already an 'app.db' file any new values added to this file
        will add on to the existing database.

        - To create a new fresh database, move the 'app.db' file and save it 
        somewhere else. DO NOT delete it. Keep it as a backup so you don't 
        lose your old database. After, running this file will make a new
        'app.db' file in this directory and will contain all the information
        currently in this file.
"""

# Creates the database using the model in db.py
# Only use the following code to create a new database.
from db import db
db.create_all()


from db import Device, Edge
# Adding Nodes to the database.
elsa = Device('Elsa', 'Node')
db.session.add(elsa)

aurora = Device('Aurora', 'Node')
db.session.add(aurora)

belle = Device('Belle', 'Node')
db.session.add(belle)

# Adding some test sensors to the database
alpha = Device('Alpha', 'Sensor')
db.session.add(alpha)

beta = Device('Beta', 'Sensor')
db.session.add(beta)

# Commit new information to the database
db.session.commit()
