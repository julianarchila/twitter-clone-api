""" User serializers. """

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, password_validation
from django.utils import timezone
from django.template.loader import render_to_string

# Django REST Framework
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from api.users.models import User, Profile
from api.users.serializers.profiles import ProfileModelSerializer

# Utilities
from datetime import timedelta
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """ User model serializer. """
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
            "following_count"
        )

    def get_following_count(self, obj):
        return obj.following.count()


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer. """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_verified:
            raise serializers.ValidationError(
                "Verify your email in order to login")

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
        self.send_confirmation_email(user)
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key

    def send_confirmation_email(self, user):
        token = self.gen_verification_token(user)
        subject = f"Welcome @{user.username}! Verify your account to start using the app."
        from_email = settings.EMAIL_HOST_USER

        content = render_to_string(
            "email_confirmation.html",
            {"token": token, "user": user}
        )

        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        exp_date = timezone.now() + timedelta(days=3)
        pay_load = {
            "user": user.username,
            "exp": int(exp_date.timestamp()),
            "type": "email_confirmation"
        }
        token = jwt.encode(pay_load, settings.SECRET_KEY, algorithm="HS256")
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer. """
    token = serializers.CharField()

    def validate_token(self, value):
        """ Validate token. """
        try:
            payload = jwt.decode(
                value, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired.")
        except jwt.PyJWTError:
            print(jwt.PyJWKError)
            raise serializers.ValidationError("Invalid token.")

        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError("Invalid token.")

        self.context["payload"] = payload
        return value

    def create(self, validated_data):
        payload = self.context.get("payload")
        user = User.objects.get(username=payload["user"])
        user.is_verified = True
        user.save()
        return user
