""" User models admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from api.users.models import User 


class CustomeUserAdmin(UserAdmin):
    """User model admin. """


admin.site.register(User, CustomeUserAdmin)
