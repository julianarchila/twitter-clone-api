"""Profile models. """

# Django
from django.db import models

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
    header = models.ImageField(
        "Profile header",
        upload_to="users/headers/",
        blank=True,
        null=True
    )

    bio = models.TextField(max_length=160, blank=True, null=True)

    def __str__(self) -> str:
        return f"Profile: {self.user.username}"