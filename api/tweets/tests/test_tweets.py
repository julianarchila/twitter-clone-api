""" Tweets tests. """

# Utils
import json

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


# Models
from api.users.models import User, Profile
from api.tweets.models import Tweet


class TweetTestApiCase(APITestCase):
    """Tweets API test case."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@test.com",
            username="testuser",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="testpassword",
        )
        self.profile = Profile.objects.create(user=self.user)

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        self.url = f"/tweets/"

    def test_tweet_create(self):
        """Test tweet create. """
        data = {
            "content": "Test tweet content",
        }
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Tweet.objects.count(), 1)

    def test_tweet_create_field_validation(self):
        """Test tweet create api validation. 
        Check if content is required.
        """
        data = {}
        request = self.client.post(self.url, data)

        self.assertEqual(request.status_code, 400)

        content = json.loads(request.content)
        self.assertEqual(
            content.get("non_field_errors"),
            ["You can't create a empty tweet."]
        )

    def test_tweet_create_auth_validation(self):
        self.client.credentials()
        data = {
            "content": "Test tweet content",
        }
        request = self.client.post(self.url, data)

        self.assertEqual(request.status_code, 401)
