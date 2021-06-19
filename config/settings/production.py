from .local import *

SECRET_KEY = env("DJANGO_SECRET_KEY")
# This is going to change to a postgres database
import dj_database_url

DATABASES = {"default": dj_database_url.config(default=env.str("DATABASE_URL"))}

STATICFILES_STORAGE = "custom_storage.static_azure.StaticAzureStorage"
