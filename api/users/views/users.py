""" User views. """

# Django REST Framework
from rest_framework import permissions
from api.users.serializers.profiles import ProfileModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from api.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
)

# Models
from api.users.models import User


class UserViewSet(GenericViewSet):
    """User view set."""

    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"

    def get_serializer_class(self):
        if self.action == "login":
            return UserLoginSerializer
        elif self.action == "signup":
            return UserSignUpSerializer
        elif self.action == "verify":
            return AccountVerificationSerializer
        else:
            return UserModelSerializer

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["profile", "me"]:
            permissions.append(IsAuthenticated)

        return [p() for p in permissions]

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "token": token}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def signup(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {"user": UserModelSerializer(user).data, "token": token}
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def verify(self, request, *args, **kwargs):
        serializers = AccountVerificationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            data={"msg": "You are now able to login"}, status=status.HTTP_202_ACCEPTED
        )

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
    def me(slef, request, *args, **kwargs):
        data = UserModelSerializer(request.user).data
        return Response(data=data, status=status.HTTP_200_OK)
