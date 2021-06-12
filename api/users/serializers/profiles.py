""" Profile serializers. """

# Django REST Framework
from rest_framework import serializers

# Models
from api.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """ Profile model serializer """
    followers_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ("picture", "bio", "header", "followers_count")

    def get_followers_count(self, obj):
        return obj.followers.count()
