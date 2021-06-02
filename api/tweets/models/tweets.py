""" Tweet models. """

# Django
from django.db import models
from django.db.models.fields import NullBooleanField

# Utils
from api.utils.models import TwModel

class Tweet(TwModel):
    """Tweet model """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="tweets/",null=True, blank=True)
    
