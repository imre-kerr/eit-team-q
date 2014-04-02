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
    ser.timeout = 3
    print "setup complete"
    return ser

def read_from_port(dongle, db):
    print "reading from port.."
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
    # TODO: Stop lying
    return "Temperature"

def handle_data(data, db):
    print data
    # Data in format "UNIT id type value", ex "UNIT 0 0 0".
    #data = data.split(" ")
    # TODO: regexp to check that data is sensor value, not setup info?
    # Currently checks for the matching list length.
    p = re.compile("UNIT \d+ \d+ \d+")
    if p.match(data):
        data = data.split(" ")
        print "extracting data and inserting to db"
        sensor_id = data[1]
        sensor_type = data[2]
        sensor_value = data[3]
        sensor = db((db.sensor.id == sensor_id)).select()
        if not sensor:
            db.sensor.insert(id=sensor_id, sensortype=type_string(sensor_type), room = 1) # Can id be set manually?
        db.sensor_reading.insert(reading = sensor_value, datetime = datetime.datetime.now(), sensor = sensor_id)
        db.commit()
    #return "<script>alert('inserted data:" + " ".join(data) + "')</script>"
