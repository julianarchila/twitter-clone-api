""" Tweets serializers. """

# Django REST Framework
from django.contrib.auth.models import User
from rest_framework import serializers, validators

# Serializers
from api.users.serializers import UserModelSerializer, UserSerializer

# Models
from api.tweets.models import Tweet


class TweetModelSerializer(serializers.ModelSerializer):
    """Tweet Base Serializer"""

    user = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    retweets = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.count()

    def get_retweets(self, obj):
        return obj.retweets.count()

    def get_liked(self, obj):
        request_user = self.context["request"].user
        if request_user == None:
            print("There is no user in the context. Please check again.")
            return False

        if not request_user.is_authenticated:
            return False
        return request_user in obj.likes.all()


class TweetSerializer(TweetModelSerializer):
    """Tweet serializer with more detail."""

    parent = TweetModelSerializer(read_only=True)


class TweetCreateSerializer(serializers.ModelSerializer):
    """Create tweet serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tweet
        fields = "__all__"

    def validate(self, data):
        if not data.get("content") and not data.get("image"):
            raise serializers.ValidationError("You can't create a empty tweet.")

        return data
