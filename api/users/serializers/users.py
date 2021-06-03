""" User serializers. """

# Django
from django.contrib.auth import authenticate

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

class UserLoginSerializer(serializers.Serializer):
    """ User login serializer. """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        self.context["user"] = user
        return data

    def create(self, validated_data):
        return self.context["user"]

