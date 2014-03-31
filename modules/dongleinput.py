#!/usr/bin/env python
# coding: utf8
# dependency: "pip install pyserial".
import serial
import time

def setup():
    ser = serial.Serial()
    ser.baudrate = 38400
    # setup input port. "python -m serial.tools.list_ports" to find the usb-port of the connected dongle.
    ser.port = "/dev/cu.usbmodem1a121"
    ser.stopbits = serial.STOPBITS_ONE
    ser.rtscts = True
    #ser.timeout = 10 #opens for 10 seconds.
    return ser
