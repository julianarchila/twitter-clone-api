""" Tweet models. """

# Django
from django.db import models

# Utils
from api.utils.models import TwModel


class TweetLike(TwModel):
    """ Tweet like model. """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    tweet = models.ForeignKey("tweets.Tweet", on_delete=models.CASCADE)


class Tweet(TwModel):
    """Tweet model """
    user = models.ForeignKey(
        "users.User", related_name="tweets", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", related_name="retweets", null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="tweets/", null=True, blank=True)
    likes = models.ManyToManyField(
        "users.User", related_name="liked_tweets", blank=True, through=TweetLike)
