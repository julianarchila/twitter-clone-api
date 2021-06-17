""" Feed urls. """

# Django
from django.urls import path

# Views
from api.feed.views import HomeFeed

urlpatterns = [
    path("feed/home/", HomeFeed.as_view()),
]
