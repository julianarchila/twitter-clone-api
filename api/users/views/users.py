""" User views. """

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from api.users import serializers

# Serializers
from api.users.serializers import UserLoginSerializer, UserModelSerializer

# Models
from api.users.models import User

class UserViewSet(GenericViewSet):
    """ User view set. """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = "username"

    @action(detail=False,methods=["POST"])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


