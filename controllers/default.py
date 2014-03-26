# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime
import time
import random
from applications.myApp.modules import dongleinput
from threading import Thread

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
#    db.house.truncate()
#    db.room.truncate()
#    db.sensor.truncate()
#    db.sensor_reading.truncate()
#    db.commit()

    # create random mock data and get current time
    a = random.uniform(15, 25)
    b = random.uniform(15, 25)
    c = random.uniform(15, 25)
    now = datetime.datetime.now()

#    db.house.insert(name='mitthus', image='<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" xml:space="preserve"><rect x="136.5" y="86.5" fill="#FFFFFF" stroke="#000000" stroke-miterlimit="10" width="700" height="350"/><rect x="141.5" y="91.5" fill="#FFFFFF" stroke="#000000" stroke-miterlimit="10" width="690" height="340"/><line fill="none" stroke="#000000" stroke-miterlimit="10" x1="335.5" y1="432" x2="335.5" y2="93"/><line fill="none" stroke="#000000" stroke-miterlimit="10" x1="622.5" y1="431" x2="622.5" y2="92"/><rect x="141.5" y="91.5" width="195" height="340" fill="rgba(0,0,0,0)" id="room1" /><rect x="622.5" y="91.5" width="195" height="340" fill="rgba(0,0,0,0)" id="room2" /></svg>')
#    db.room.insert(name='kjøkken', image='<rect x="141.5" y="91.5" width="194" height="340" fill="rgba(0,0,0,0)" id="room1" />', xpos=142, ypos=92, house = db(db.house.name=='mitthus').select()[0])
#    db.room.insert(name='bad', image='<rect x="622.5" y="91.5" width="210" height="340" fill="rgba(0,0,0,0)" id="room2" />', xpos=623, ypos=92, house = db(db.house.name=='mitthus').select()[0])
#    db.room.insert(name='stue', image='<rect x="335.5" y="91.5" width="287" height="340" fill="rgba(0,0,0,0)" id="room3" />', xpos=336, ypos=92, house = db(db.house.name=='mitthus').select()[0])

    room = db().select(db.room.ALL)[0]
#    db.sensor.insert(sensortype = 'Temperature', room = room)

    room = db().select(db.room.ALL)[1]
#    db.sensor.insert(sensortype = 'Temperature', room = room)
#    db.sensor.insert(sensortype = 'Light', room = room)

    room = db().select(db.room.ALL)[2]
#    db.sensor.insert(sensortype = 'Temperature', room = room)

    # select sensor to assign reading to (TODO: find a better way to do this)
    sensors = db(db.sensor.sensortype =='Temperature').select()

    # insert sensor reading into database

    db.sensor_reading.insert(reading = a, datetime = now, sensor = sensors[0])
    db.sensor_reading.insert(reading = b, datetime = now, sensor = sensors[1])
    db.sensor_reading.insert(reading = c, datetime = now, sensor = sensors[2])

    light_sensors = db(db.sensor.sensortype =='Light').select()
    db.sensor_reading.insert(reading = random.uniform(-1, 1), datetime = now, sensor = light_sensors[0])

    # create some variables for the index.html view
    sensorreading = db().select(db.sensor_reading.ALL, orderby=db.sensor_reading.id)
    sensor = db().select(db.sensor.ALL, orderby=db.sensor.id)
    room = db().select(db.room.ALL)
    house = db().select(db.house.ALL)
    return locals()

def sensors():
    return dict(sensorreading = db().select(db.sensor_reading.ALL, orderby=db.sensor_reading.id))

def map():
    data = dict()
    data['room'] = db().select(db.room.ALL)
    data['sensor'] = db().select(db.sensor.ALL)
    data['sensorreading'] = db().select(db.sensor_reading.ALL)
    return dict(data = data)

@auth.requires_login()
def touchroom():
    isOpen = False
    dongle = dongleinput.setup()
    dongle.open()
    isOpen = dongle.isOpen()
    t1 = Thread(target = readDongleInput(dongle))
    t1.start()
    #--------------#
    return dict(isOpen = isOpen)

def readDongleInput(dongle):
    i = 0
    while(i < 1):
        line = dongle.readline()
        data = line.split(" ")
        sensor_id = data[1]
        sensor_type = data[2]
        sensor_value = data[3]
        db.sensor_reading.insert(reading = sensor_value, datetime = datetime.datetime.now(), sensor = sensor_type)
        i += 1
        #time.sleep(3)

def calcAverageTemp():
    # calculating overall average temperature
    average_temp = 0
    readings = []
    datetimes = []
    sensorreadings = db().select(db.sensor_reading.ALL, orderby=db.sensor_reading.id)
    for s in sensorreadings:
        average_temp += s.reading
        readings.append(s.reading)
        datetimes.append(s.datetime)
    average_temp = average_temp / len(sensorreadings)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
