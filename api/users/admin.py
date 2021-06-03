""" User models admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from api.users.models import User, Profile


class CustomeUserAdmin(UserAdmin):
    """User model admin. """
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_verified")
    list_filter = ("is_staff", "created", "modified")


admin.site.register(User, CustomeUserAdmin)

admin.site.register(Profile)