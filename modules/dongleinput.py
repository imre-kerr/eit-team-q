#!/usr/bin/env python
# coding: utf8
# dependency: "pip install pyserial".
import serial
import time
import datetime

def setup():
    ser = serial.Serial()
    ser.baudrate = 38400
    # setup input port. "python -m serial.tools.list_ports" to find the usb-port of the connected dongle.
    ser.port = "/dev/cu.usbmodem1a121"
    ser.stopbits = serial.STOPBITS_ONE
    ser.rtscts = True
    ser.timeout = 4 #opens for 2 seconds.
    return ser

def read_from_port(dongle,db):
    #while True:
        #print("reading from com-port..")
    reading = dongle.readline()
    handle_data(reading, db)

def handle_data(data, db):
    # Data in format "UNIT id type value", ex "UNIT 0 0 0".
    data = data.split(" ")
    # TODO: regexp to check that data is sensor value, not setup info?
    # Currently checks for the matching list length.
    if len(data) == 4:
        sensor_id = data[1]
        sensor_type = 64 #data[2]
        sensor_value = data[3]
        db.sensor_reading.insert(reading = sensor_value, datetime = datetime.datetime.now(), sensor = sensor_type)
    return "<script>console.log('inserted data:" + " ".join(data) + "')</script>"
    
#dongle = setup()
#dongle.open()
#read_from_port(dongle)
