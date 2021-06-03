""" User serializers. """

# Django
from django.contrib.auth import authenticate, password_validation

# Django REST Framework
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from api.users.models import User, Profile
from api.users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer. """
    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "profile"
        )


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer. """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        self.context["user"] = user
        return data

    def create(self, validated_data):
        user = self.context["user"]
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key

class UserSignUpSerializer(serializers.Serializer):
    """ User signup serializer. 
    Handles data validation and user/profile creation.
    """
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this email already exists."
            )
        ]
    )
    username = serializers.CharField(
        min_length=2,
        max_length=40,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This username is already taken"
            )
        ]
    )

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Password 
    password = serializers.CharField(min_length=8, max_length=200)
    password_confirmation = serializers.CharField(min_length=8, max_length=200)

    def validate(self, data):
        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match.")

        password_validation.validate_password(password=password)

        return data

    def create(self, data):
        data.pop("password_confirmation")
        # Create user
        user = User.objects.create_user(**data, is_staff=False)

        # Create user's objects
        Profile.objects.create(user=user)

        token, created = Token.objects.get_or_create(user=user)

        return user, token.key