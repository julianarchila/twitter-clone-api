from storages.backends.azure_storage import AzureStorage
from config.settings.base import env


class StaticAzureStorage(AzureStorage):
    account_name = "twitterclonestorage"
    account_key = env.str("AZURE_ACCOUNT_KEY")
    azure_container = "static"
    expiration_secs = None
