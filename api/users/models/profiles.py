"""Profile models. """

# Django
from django.db import models
from django.db.models.fields import NullBooleanField

# Utils
from api.utils.models import TwModel

class Profile(TwModel):
    """ Profile model. """
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    picture = models.ImageField(
        "Profile picture",
        upload_to="users/pictures/",
        blank=True,
        null=True
    )
    picture = models.ImageField(
        "Profile header",
        upload_to="users/headers/",
        blank=True,
        null=True
    )

    bio = models.TextField(max_length=160)