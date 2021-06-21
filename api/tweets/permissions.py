""" Tweets permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsTweetOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
