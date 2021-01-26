import xarray as xr
import geojson
import json
import numpy
from geojson import Point,Feature,FeatureCollection
from integr import getDataFileRecord

def nc2jsonPoint(parameterName,date,time,lat,lng):
	#req_data = request.get_json()
	#parameterNameReceived = req_data['parameterName']
	parameterNameReceived = parameterName


	f = open('apicodes.json')
	apicodes = json.load(f)
	f.close()
	parameterInfo = apicodes[parameterNameReceived]
	parameterName = parameterInfo['name']
	#date = req_data['date']
	fileName = getDataFileRecord("copernicus", date,0)
	requestedLat = lat #float(req_data['lat'])
	requestedLng = lng #float(req_data['lng'])
	dt= xr.open_dataset(fileName)
	var = dt[parameterName]
	var = var.sel(time=date,method="nearest").squeeze()

	latitudes = var.coords['latitude'].values.tolist()
	longitudes = var.coords['longitude'].values.tolist()

	latIndex=0
	lngIndex=0
	for i in range(len(latitudes)):
		if latitudes[i]>=requestedLat:
			break
		else:
			latIndex+=1

	for i in range(len(longitudes)):
		if longitudes[i]>=requestedLng:
			break
		else:
			lngIndex+=1

	val = var.loc[dict(latitude=latitudes[latIndex],longitude=longitudes[lngIndex])]
	pointValue = Point((longitudes[lngIndex],latitudes[latIndex]))
	dataValue = val.values
	feature = Feature(geometry=pointValue,properties={parameterName:dataValue})
	return feature

def nc2json(parameterName,date,time):
	#req_data = request.get_json()
	#parameterNameReceived = req_data['parameterName']
	parameterNameReceived = parameterName


	f = open('apicodes.json')
	apicodes = json.load(f)
	f.close()
	parameterInfo = apicodes[parameterNameReceived]
	parameterName = parameterInfo['name']
	#date = req_data['date']
	fileName = getDataFileRecord("copernicus", date,0)
	dt= xr.open_dataset(fileName)
	var = dt[parameterName]
	var = var.sel(time=date,method="nearest").squeeze()
	feature_list = []
	for i in var.coords['latitude'].values.tolist():
		for j in var.coords['longitude'].values.tolist():
			val = var.loc[dict(latitude=i,longitude=j)]
			pointValue = Point((j,i))
			dataValue = val.values
			featureAdded = Feature(geometry=pointValue,properties={parameterName:dataValue})
			feature_list.append(featureAdded)
	
	feature_collection= FeatureCollection(feature_list)
	return feature_collection
