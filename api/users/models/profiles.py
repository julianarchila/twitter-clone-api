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
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    followers = models.ManyToManyField(
        "users.User", related_name='following', blank=True)
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self) -> str:
        return f"Profile: {self.user.username}"
