# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Utils
from api.utils.models import TwModel

class User(TwModel,AbstractUser):
    """ Custom user model. """
    email = models.EmailField(
        "email adress",
        unique=True,
        error_messages={
            "unique": "A user with that email already exists."
        }
        )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_verified = models.BooleanField(
        "Verified",
            default=False,
            help_text="Set true when user has verified its email adress."
        )

    def __str__(self):
            return self.username

    def get_short_name(self):
        return self.username
