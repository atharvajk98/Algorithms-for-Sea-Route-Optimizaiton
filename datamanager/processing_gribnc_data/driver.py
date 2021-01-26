import geojson
import requests
fileName = input("Enter Filename:")
parameterName = input("Enter Parameter Name:")
parameterName = parameterName.lower().capitalize()
typeOfLevelName = input("Enter type of level:")
levelName = input("Enter level:")
levelVal = int(levelName)
foreCastHourName = input("Enter forecast hour:")
forecastHour = int(foreCastHourName)
myjson = {
	"fileName":fileName,
	"parameterName":parameterName,
	"forecastHour":forecastHour
   }
mygeojson = requests.post("http://127.0.0.1:5000/get-geo",json=myjson)
mygeojson = mygeojson.json()
with open("grib2geo.json","w") as write_file:
    geojson.dump(mygeojson,write_file)
