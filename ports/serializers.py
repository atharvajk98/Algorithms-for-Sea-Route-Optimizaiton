from rest_framework import serializers
from .models import NavalPort

class NavalPortSerializer(serializers.ModelSerializer):
	class Meta:
		model = NavalPort
		fields = ['world_port_index','main_port_name','wpi_country','region','lat','lon']