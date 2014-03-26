#!/usr/bin/env python
# coding: utf8
# dependency: pyserial, "pip install pyserial".
import serial
import time

def setup():
    ser = serial.Serial()
    ser.baudrate = 38400
    # setup input port. "python -m serial.tools.list_ports" to find the usb-port of the connected dongle.
    ser.port = "/dev/cu.usbmodem1a121"
    ser.stopbits = serial.STOPBITS_ONE
    ser.rtscts = True
    ser.timeout = 3
    return ser

"""
def getSingle(ser):
    # Reads one line, splits at a new line.
    x = ser.readline()
    # Data kommer i format: "UNIT ID sensortype data", for eksempel: "UNIT 1 0 20". La oss forsøke å lese hele linja og splitte på " ".
    data = x.split(" ")
    # Hvis det kommer noe annet enn UNIT er det snakk om config-meldinger i starten av oppsettet.
    if (data[0] == "UNIT"):
        sensor_id = data[1]
        sensor_type = data[2]
        sensor_value = data[3]
    return x

def listen(ser):
    while(True):
        getSingle(ser)
        time.sleep(3)
"""
