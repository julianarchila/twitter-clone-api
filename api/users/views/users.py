""" User views. """

# Django REST Framework
from api.tweets import serializers
from decimal import Context
from django.db.models.fields import FloatField
from rest_framework import permissions
from api.users.serializers.profiles import ProfileModelSerializer
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from api.users.serializers import UserModelSerializer, FollowSerializer

# Models
from api.users.models import User


class UserViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    """User view set."""

    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"

    def get_serializer_class(self):
        return UserModelSerializer

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["profile"]:
            permissions.append(IsAuthenticated)

        return [p() for p in permissions]

    @action(detail=False, methods=["PUT", "PATCH"])
    def profile(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = ProfileModelSerializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def follow(self, request, *args, **kwargs):
        """Toggle follow endpoint."""

        serializer = FollowSerializer(
            data=request.query_params, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        user, following = serializer.save()
        data = {
            "following": following,
            "user": UserModelSerializer(user).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
