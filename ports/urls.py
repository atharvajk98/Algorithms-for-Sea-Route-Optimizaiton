from django.urls import include, path
from .views import NavalPortsList

urlpatterns = [
	path('naval',NavalPortsList.as_view())
]