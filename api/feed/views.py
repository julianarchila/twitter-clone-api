""" Feed views. """

# Django REST Framework
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Serializers
from api.tweets.serializers import TweetSerializer

# Models
from api.users.models import User
from api.tweets.models import Tweet


class HomeFeed(GenericAPIView):
    """Home feed view."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get all user tweets
        tweets = user.tweets.all()

        # Get tweets from users current user follows
        following = user.following.all()
        more_tweets = Tweet.objects.filter(user__profile__in=following)

        # Mix tweets and order by most recent
        tweets |= more_tweets
        tweets = tweets.order_by("-created")

        serializer = TweetSerializer(
            tweets, many=True, context=self.get_serializer_context()
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfileFeed(GenericAPIView):
    "User profile feed view."
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(username=request.query_params.get("u"))
        except User.DoesNotExist:
            return Response(
                data={"message": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tweets = user.tweets.all().order_by("-created")
        serializer = TweetSerializer(
            tweets, many=True, context=self.get_serializer_context()
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)
