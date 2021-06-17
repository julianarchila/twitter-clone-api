""" Profile serializers. """

# Django REST Framework
from rest_framework import serializers

# Models
from api.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer"""

    class Meta:
        model = Profile
        fields = ("picture", "bio", "header")
