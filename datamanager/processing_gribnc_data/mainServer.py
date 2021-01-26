from flask import Flask, request
from gribModule import grib2json,grib2jsonPoint
from ncModule import nc2json,nc2jsonPoint
app = Flask(__name__)



	

@app.route('/',methods=['GET'])
def home():
    return "<h1>Hello!</h1>"

@app.route('/get-geo',methods=['POST'])
def serveRequest(parameterName,date,time):
	#req_data = request.get_json()
	#parameterName = req_data['parameterName']
	if parameterName=='iceConcentration' or parameterName=='temperature' or parameterName=='northwardCurrentVelocity' or parameterName=='eastwardCurrentVelocity':
		return nc2json(parameterName,date,time)		
	else:
		return grib2json(parameterName,date,time)


@app.route('/get-single',methods=['POST'])
def servePointRequest(parameterName,date,time,lat,lng):
	#req_data = request.get_json()
	#parameterName = req_data['parameterName']
	if parameterName=='iceConcentration' or parameterName=='temperature' or parameterName=='northwardCurrentVelocity' or parameterName=='eastwardCurrentVelocity':
		return nc2jsonPoint(parameterName,date,time,lat,lng)		
	else:
		return grib2jsonPoint(parameterName,date,time,lat,lng)


