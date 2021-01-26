import pygrib
import geojson
import numpy
import json
from geojson import Point,Feature,FeatureCollection
from integr import getDataFileRecord
import datetime
def grib2json(parameterName,date,time):
    #req_data = request.get_json()
    #parameterNameReceived = req_data['parameterName']
    parameterNameReceived = parameterName



    f = open('apicodes.json')
    apicodes = json.load(f)
    f.close()
    parameterInfo = apicodes[parameterNameReceived]
    parameterName = parameterInfo['name']
    typeOfLevelName = parameterInfo['typeOfLevel']
    level = int(parameterInfo['level'])
    parameterSource = parameterInfo['source']
    #requestedDate = req_data['date']
    requestedDate = date
    #requestedHour = int(req_data['hour'])
    requestedHour = int(time)
    fileRecord = getDataFileRecord(parameterSource,requestedDate,requestedHour)
    if fileRecord == "OUTOFRANGE":
        return "Data for the given Date not available yet!"
    if fileRecord == "NOTFOUND":
        return "Data File Not Found!"

    fileName = fileRecord['File_Path']
    difference = datetime.datetime.strptime(requestedDate,"%Y%m%d") - datetime.datetime.strptime(fileRecord['Issue_date'],"%Y%m%d")
    totalHours = (difference.total_seconds()//3600) + requestedHour
    grbs = pygrib.open(fileName)
    grb = grbs.select(name=parameterName,typeOfLevel=typeOfLevelName,level=level,step=totalHours)[0]
    data = grb['values']
    if type(data) is numpy.ma.core.MaskedArray:
        data = data.filled()
    distinctLatitudes = grb['distinctLatitudes']
    distinctLongitudes = grb['distinctLongitudes']
    feature_list = []
    for i in range(distinctLatitudes.shape[0]):
        for j in range(distinctLongitudes.shape[0]):
            pointValue = Point((distinctLongitudes[j],distinctLatitudes[i]))
            dataValue = data[i][j]
            featureAdded = Feature(geometry=pointValue,properties={parameterName:dataValue})
            feature_list.append(featureAdded)
    feature_collection= FeatureCollection(feature_list)
    grbs.close()
    return feature_collection


def grib2jsonPoint(parameterName,date,time,lat,lng):
    #req_data = request.get_json()
    #parameterNameReceived = req_data['parameterName']
    parameterNameReceived = parameterName

    f = open('apicodes.json')
    apicodes = json.load(f)
    f.close()
    parameterInfo = apicodes[parameterNameReceived]
    parameterName = parameterInfo['name']
    typeOfLevelName = parameterInfo['typeOfLevel']
    level = int(parameterInfo['level'])
    parameterSource = parameterInfo['source']
    #requestedDate = req_data['date']
    requestedDate = date
    #requestedHour = int(req_data['hour'])
    requestedHour = int(time)
    fileRecord = getDataFileRecord(parameterSource,requestedDate,requestedHour)
    if fileRecord == "OUTOFRANGE":
        return "Data for the given Date not available yet!"
    if fileRecord == "NOTFOUND":
        return "Data File Not Found!"
    fileName = fileRecord['File_Path']
    difference = datetime.datetime.strptime(requestedDate,"%Y%m%d") - datetime.datetime.strptime(fileRecord['Issue_date'],"%Y%m%d")
    totalHours = (difference.total_seconds()//3600) + requestedHour
    grbs = pygrib.open(fileName)

    requestedLat = lat #float(req_data['lat'])
    requestedLng = lng #float(req_data['lng'])
    try:
        grb = grb = grbs.select(name=parameterName,typeOfLevel=typeOfLevelName,level=level,step=totalHours)[0]
        data = grb['values']
        if type(data) is numpy.ma.core.MaskedArray:
            data = data.filled()
        distinctLatitudes = grb['distinctLatitudes']
        distinctLongitudes = grb['distinctLongitudes']

        latIndex = 0
        lngIndex = 0
        for i in range(distinctLatitudes.shape[0]):
            if distinctLatitudes[i]>=requestedLat:
                break
            else:
                latIndex+=1
        
        for i in range(distinctLongitudes.shape[0]):
            if distinctLongitudes[i]>=requestedLng:
                break
            else:
                lngIndex+=1

        pointValue = Point((distinctLongitudes[lngIndex],distinctLatitudes[latIndex]))
        dataValue = data[latIndex][lngIndex]
        feature = Feature(geometry=pointValue,properties={parameterName:dataValue})
        return feature
    except ValueError:
        print("Record not found!")
    finally:
        grbs.close()
