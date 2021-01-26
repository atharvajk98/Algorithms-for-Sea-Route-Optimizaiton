from django.urls import include, path
from .views import WeatherAPI

urlpatterns = [
	path('weather',WeatherAPI.as_view())
]