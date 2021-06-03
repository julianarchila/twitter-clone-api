""" Tweets serializers. """

# Django REST Framework
from django.contrib.auth.models import User
from rest_framework import serializers, validators

# Serializers
from api.users.serializers import UserModelSerializer

# Models
from api.tweets.models import Tweet

class TweetModelSerializer(serializers.ModelSerializer): 
    """ Tweet model serializer. """
    user = UserModelSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = "__all__"

class TweetCreateSerializer(serializers.ModelSerializer):
    """ Create tweet serializer. """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Tweet
        fields = "__all__"

    def validate(self, data):
        if not data.get("content") and not data.get("image"):
            raise serializers.ValidationError("You can't create a empty tweet.")
        
        return data

