from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.rest.serializers import UserSerializer, GroupSerializer, RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    payload = {}
    if serializer.is_valid():
        user = serializer.save()
        return Response(data=payload,status=status.HTTP_200_OK)
    return Response(data=payload,status=500)

@api_view(['POST'])
def login(request):
    # serializer = RegistrationSerializer(data=request.data)
    data = {}
    payload = {}
    user = authenticate(request, username=request.data['username'], password=request.data['password'])
    if user:
        return Response(data={'status':True},status=status.HTTP_200_OK)
    return Response(data={'status':False},status=status.HTTP_200_OK)



@api_view(['GET'])
def test(request):
    from datetime import datetime
    