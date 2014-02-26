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
import random

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

    # create random mock data and get current time
    a = random.uniform(15, 25)
    now = datetime.datetime.now()

#    db.house.insert(name='mitthus')

#    db.room.insert(name='stue', house = db(db.house.name=='mitthus').select()[0])

    # select house and room (should be a better way to do this)
    houses = db(db.house.name=='mitthus').select()
    house = houses[0]
    rooms = db(db.room.name=='stue').select()
    room = rooms[0]

    # insert sensor reading into database
    db.sensor.insert(name = 'Sensor 1', sensor_type = 'Temperature', sensor_reading = a, date_time = now, room = room, house = house)

    # create some variables for the index.html view
    sensor = db().select(db.sensor.ALL, orderby=db.sensor.id)
    room = db().select(db.room.ALL)
    house = db().select(db.house.ALL)
    return locals()

@auth.requires_login()
def touchroom():
    sensors = db().select(db.sensor.ALL, orderby=db.sensor.id)
    # calculating overall average temperature
    average_temp = 0
    readings = []
    datetimes = []
    for s in sensors:
        average_temp += s.sensor_reading
        readings.append(s.sensor_reading)
        datetimes.append(s.date_time)
    average_temp = average_temp / len(sensors)
    return dict(average_temp = average_temp, readings = readings, datetimes = datetimes)

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
