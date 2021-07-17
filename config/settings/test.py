""" Testing settings.

With these settings, tests run faster.
"""

from .base import *
from .base import env

# Base
DEBUG = False
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="7lEaACt4wsCj8JbXYgQLf4BmdG5QbuHTMYUGir2Gc1GHqqb2Pv8w9iXwwlIIviI2"
)

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": ""
    }
}

# Passwords
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
