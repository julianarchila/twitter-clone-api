""" User serializers. """


# Django REST Framework
from rest_framework import serializers

# Models
from api.users.models import User
from api.users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "profile",
            "following_count",
        )

    def get_following_count(self, obj):
        return obj.following.count()


class FollowSerializer(serializers.Serializer):
    """Follow action serializer."""

    user = serializers.CharField()

    def validate_user(self, data):
        try:
            user = User.objects.get(username=data)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user == self.context["user"]:
            raise serializers.ValidationError("You can't follow yourself.")
        return user

    def create(self, validated_data):
        user = validated_data["user"]
        current_user = self.context.get("user")
        if user.profile.followers.filter(id=current_user.id).exists():
            current_user.following.remove(user.profile)
            following = False
        else:
            current_user.following.add(user.profile)
            following = True
        current_user.save()

        return user, following
