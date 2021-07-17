""" User model test. """

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework.test import APITestCase

# Models
from api.users.models import User


class UserModelTestCase(TestCase):
    """ Tests for the User model. """

    def setUp(self) -> None:
        """ Test case setup."""
        return super().setUp()

    def test_user_creation(self):
        """Test the creation of a user. """
        User.objects.create_user(
            email="user@test.com",
            username="testuser",
            first_name="TestFirstName",
            last_name="TestLastName",
            password="testpassword",
        )

        self.assertEqual(User.objects.count(), 1)
