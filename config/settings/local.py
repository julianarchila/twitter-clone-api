from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2k%=^z7^zt+-m*%sy)*uv2c*2y#nzytoep#)16$!o=az2d2)9#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS += ["django_extensions"]


DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"

AZURE_ACCOUNT_NAME = "twitterclonestorage"
AZURE_CONTAINER = "media"
AZURE_ACCOUNT_KEY = env.str("AZURE_ACCOUNT_KEY")
