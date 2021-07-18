""" Tweet actions test. (like, retweet, etc.) """

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


# Models
from api.users.models import User, Profile
from api.tweets.models import Tweet


class TweetActionsAPITestCase(APITestCase):
    """Test tweet actions endpoints. """

    def setUp(self) -> None:
        # Create a user
        self.user = User.objects.create_user(
            email="user@test.com",
            username="testuser",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="testpassword",
        )
        self.profile = Profile.objects.create(user=self.user)

        self.tweet = Tweet.objects.create(user=self.user, content="Test tweet")

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_like_tweet(self):
        """ Test like tweet. """

        url = "/tweets/like/"
        # Like tweet
        response = self.client.post(url, {"tweet": self.tweet.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("liked"), True)

        # Unlike tweet
        response = self.client.post(url, {"tweet": self.tweet.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("liked"), False)

    def test_retweet_tweet(self):
        """ Test retweet tweet. """
        url = "/tweets/retweet/"
        # Retweet tweet
        response = self.client.post(url, {"parent": self.tweet.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("retweet"), True)
        self.assertEqual(
            response.data.get("parent").get("id"),
            str(self.tweet.id)
        )

    def test_delete_tweet(self):
        """Test delete tweet"""
        url = f"/tweets/{self.tweet.id}/"
        response = self.client.delete(url)

        # Check response
        self.assertEqual(response.status_code, 204)

        # Check tweet deleted in database
        self.assertEqual(Tweet.objects.filter(id=self.tweet.id).count(), 0)
