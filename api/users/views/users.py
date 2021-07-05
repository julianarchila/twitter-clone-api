""" User views. """

# Django REST Framework
from api.users.serializers.profiles import ProfileModelSerializer
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from api.users.serializers import UserModelSerializer, FollowSerializer, UserSerializer

# Models
from api.users.models import User


class UserViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """User view set."""

    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"
    search_fields = ["username"]
    filter_backends = [SearchFilter]
    queryset = User.objects.filter(is_active=True).order_by("profile__followers__count")

    def get_serializer_class(self):
        if self.action == "profile":
            return ProfileModelSerializer
        elif self.action == "follow_toggle":
            return FollowSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        permissions = [AllowAny]
        if self.action in ["profile"]:
            permissions.append(IsAuthenticated)

        return [p() for p in permissions]

    def list(self, request, *args, **kwargs):
        if not request.query_params.get("search", None):
            return Response(
                {"message": "no search param"}, status=status.HTTP_400_BAD_REQUEST
            )

        return super().list(self, request, *args, **kwargs)

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

    @action(detail=False, methods=["POST"])
    def follow_toogle(self, request, *args, **kwargs):
        """Toggle follow endpoint."""

        serializer = FollowSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        user, following = serializer.save()
        data = {
            "following": following,
            "user": UserModelSerializer(user).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
