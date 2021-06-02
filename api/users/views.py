""" User views. """

# Django REST Framework
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Serializers
from api.users.serializers import UserLoginSerializer

class UserViewSet(GenericViewSet):
    """ User view set. """
    @action(detail=False,methods="POST")
    def login(self, request, *args, **kwargs):

