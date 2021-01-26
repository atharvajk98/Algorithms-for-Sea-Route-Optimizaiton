from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'password', 'username', 'email', 'groups']
		# extra_kwargs = {
		# 		'password':{'write_only': True}
		# 	}
	def save(self):
		user = super().save()
		user.set_password(self.validated_data['password'])
		user.save()
		return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ['url', 'name']


class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password', 'email']

	def save(self):
		print(self.validated_data)
		user = User(
			email=self.validated_data['email'],
			username=self.validated_data['username']
			)
		user.set_password(self.validated_data['password'])
		user.save()
		return user


	