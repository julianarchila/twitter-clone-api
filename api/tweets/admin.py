""" Tweets admin. """

# Django
from django.contrib import admin

# Models
from api.tweets.models import Tweet

admin.site.register(Tweet)