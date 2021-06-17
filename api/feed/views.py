""" Feed views. """

# Django REST Framework
from django.utils.regex_helper import contains
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.tweets import serializers

# Serializers
from api.tweets.serializers import TweetSerializer


class HomeFeed(GenericAPIView):
    """Home feed view."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tweets = list(user.tweets.all())
        for p in user.following.all():
            for t in p.user.tweets.all():
                print(t)
                tweets.append(t)

        serializer = TweetSerializer(
            tweets, many=True, context=self.get_serializer_context()
        )
        return Response(data=serializer.data, status=200)
