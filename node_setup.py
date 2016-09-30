from db import db
from db import *


# def add_Device(node_id):
#     """
#     """

#     nodes = Device.query.filter_by(d_type='Node').order_by(Device.label).all()
#     sensors = Device.query.filter_by(d_type='Sensor').order_by(Device.label).all()

#     print nodes
#     print sensors

nodes = Device.query.filter_by(d_type='Node').order_by(Device.label).all()
sensors = Device.query.filter_by(d_type='Sensor').order_by(Device.label).all()

print nodes
print sensors


node1 = nodes[0]

nodeid = node1.id

print nodeid

# ad = ActivatedDevices(nodeid)
# db.session.add(ad)
# db.session.commit()

select = Device.query.filter_by(id=2).all()

print select

activated_devices = ActivatedDevices.query.all()

print activated_devices



# SELECT d.id, d.label, d.d_type FROM ActivatedDevices a, Device d
# WHERE a.device_id==d.id