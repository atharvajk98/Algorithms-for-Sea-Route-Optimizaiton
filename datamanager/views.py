from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import requests

class WeatherAPI(APIView):
	
	def get(self,request):
		lat = float(request.query_params.get('lat'))
		lon = float(request.query_params.get('lat'))
		api_call = "http://api.openweathermap.org/data/2.5/forecast/daily?lat={0:.2f}&lon={0:.2f}&cnt=16&appid=0e1c13da68ef589d01f908ba37938efd".format(lat,lon)
		response = requests.get(api_call)
		return Response(data=response.json(),status=response.status_code)
