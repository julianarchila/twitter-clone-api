""" Feed urls. """

# Django
from django.urls import path

# Views
from api.feed.views import HomeFeed, ProfileFeed

urlpatterns = [
    path("feed/home/", HomeFeed.as_view()),
    path("feed/profile/", ProfileFeed.as_view()),
]
