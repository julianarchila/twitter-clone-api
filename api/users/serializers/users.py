""" User serializers. """

# Django REST Framework
from django.db.models import fields
from rest_framework import serializers

# Models
from api.users.models import User 

class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer. """
    class Meta:
        model = User
        fields = "__all__"

class UserLoginSerializer(serializers.ModelSerializer):
    """ User login serializer. """
    class Meta:
        model = User
        fields = ("")
