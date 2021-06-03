"""Tweet actions serializers. """

# Django REST Framework
from rest_framework import serializers

# Serializers
from api.tweets.serializers import TweetModelSerializer

# Models
from api.tweets.models import TweetLike, Tweet

class LikeTweetSerializer(serializers.Serializer):
    """ Like tweet serializer. """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tweet = serializers.IntegerField()

    def validate_tweet(self, data):
        try:
            tweet = Tweet.objects.get(id=data)
        except Tweet.DoesNotExist:
            raise serializers.ValidationError("Tweet not found.")
        
        return tweet

    def create(self, validated_data):
        user = validated_data["user"]
        tweet = validated_data["tweet"]

        if TweetLike.objects.filter(user=user, tweet=tweet).exists():
            tweet.likes.remove(user)
        else:
            tweet.likes.add(user)

        return tweet

