""" Tweet models. """

# Django
from django.db import models
from django.db.models.fields import NullBooleanField


class Tweet(models.Model):
    """Tweet model """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
