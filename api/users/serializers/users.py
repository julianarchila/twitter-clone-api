""" User serializers. """


# Django REST Framework
from rest_framework import serializers

# Models
from api.users.models import User
from api.users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "profile",
            "following_count",
        )

    def get_following_count(self, obj):
        return obj.following.count()
