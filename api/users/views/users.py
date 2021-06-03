""" User views. """

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from api.users import serializers

# Serializers
from api.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer
)

# Models
from api.users.models import User


class UserViewSet(GenericViewSet):
    """ User view set. """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = "username"

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserModelSerializer(user).data,
            "token": token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def signup(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserModelSerializer(user).data,
            "token": token
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

