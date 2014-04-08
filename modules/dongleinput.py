#!/usr/bin/env python
# coding: utf8
# dependency: "pip install pyserial".
import serial
import time
import datetime
import re
        
def setup():
    ser = serial.Serial()
    ser.baudrate = 38400
    # setup input port. "python -m serial.tools.list_ports" to find the usb-port of the connected dongle.
    ser.port = "/dev/cu.usbmodem1a121"
    ser.stopbits = serial.STOPBITS_ONE
    ser.rtscts = True
    ser.timeout = 0.2
    #print "setup complete"
    return ser

def read_from_port(dongle, db):
    #print "reading from port.."
    '''
    if not dongle:
        print  "dongle not setup"
        dongle = setup()
    if not dongle.isOpen():
        print "opening dongle."
        dongle.open()
    '''
    reading = dongle.readline()
#dongle.close()
    return handle_data(reading, db)

def type_string(type):
    if (type == 1):
        return "Temperature"
    elif (type == 2):
        return "Light"
    else:
        return "Other"

def id_to_room(sensor_id):
    return {
         211: 1,
         93: 2,
         250: 3,
         }.get(sensor_id, 4)

def handle_data(data, db):
    print data
    # Data in format "UNIT id type value", ex "UNIT 250 1 26".
    #data = data.split(" ")
    p = re.compile("UNIT \d+ \d+ \d+")
    if p.match(data):
        data = data.split(" ")
        #print "extracting data and inserting to db"
        sensor_id = int(data[1])
        sensor_type = int(data[2])
        sensor_value = int(data[3])
        sensor = db((db.sensor.id == sensor_id+sensor_type)).select()
        temp = (sensor_id+sensor_type)
        #print "temp er :" + str(temp)
        db.sensor_reading.insert(reading = sensor_value, datetime = datetime.datetime.now(), sensor = temp)
        db.commit()
    #return "<script>alert('inserted data:" + " ".join(data) + "')</script>"