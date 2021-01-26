from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from ports.models import NavalPort
from .serializers import NavalPortSerializer
# Create your views here.

from rest_framework import generics
class NavalPortsList(generics.ListAPIView):
	serializer_class = NavalPortSerializer
	
	def get_queryset(self):
		query = self.request.query_params.get('q')
		lookups= Q(main_port_name__icontains=query) | Q(world_port_index__icontains=query)
		return NavalPort.objects.filter(lookups)
