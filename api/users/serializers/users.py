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
    followers_count = serializers.SerializerMethodField(read_only=True)

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
            "followers_count",
        )

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.profile.followers.count()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    followers_count = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "profile",
            "first_name",
            "last_name",
            "following_count",
            "followers_count",
            "following",
        )

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.profile.followers.count()

    def get_following(self, obj):
        request_user = self.context["request"].user
        if request_user == None:
            print("There is no user in the context. Please check again.")
        return obj.profile in request_user.following.all()


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
