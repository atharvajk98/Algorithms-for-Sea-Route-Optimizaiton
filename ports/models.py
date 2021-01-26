from django.db import models
from django.db.models.signals import post_migrate
import pandas as pd
import logging

class NavalPort(models.Model):	
	world_port_index = models.IntegerField()
	main_port_name = models.CharField(max_length=100)
	wpi_country = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	lat = models.FloatField()
	lon = models.FloatField()