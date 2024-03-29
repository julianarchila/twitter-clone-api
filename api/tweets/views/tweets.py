""" Tweets views. """

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import IsAuthenticated
from api.tweets.permissions import IsTweetOwner

# Serializers
from api.tweets.serializers import (
    TweetSerializer,
    TweetCreateSerializer,
    LikeTweetSerializer,
    RetweetSerializer,
)

# Models
from api.tweets.models import Tweet


class TweetViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Tweet view set."""

    queryset = Tweet.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return TweetCreateSerializer
        elif self.action == "like":
            return LikeTweetSerializer
        elif self.action == "retweet":
            return RetweetSerializer
        else:
            return TweetSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action == "destroy":
            permissions.append(IsTweetOwner)
        return [p() for p in permissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tweet = serializer.save()
        data = TweetSerializer(
            tweet, context=self.get_serializer_context()).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def like(self, request, *args, **kwargs):
        """Handles like toogle."""
        serializer = LikeTweetSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        tweet = serializer.save()
        data = TweetSerializer(
            tweet, context=self.get_serializer_context()).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def retweet(self, request, *args, **kwargs):
        serializer = RetweetSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        tweet = serializer.save()
        data = TweetSerializer(
            tweet, context=self.get_serializer_context()).data
        return Response(data=data, status=status.HTTP_201_CREATED)
