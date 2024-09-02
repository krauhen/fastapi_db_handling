import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

secret_client = None


def get_secret_client():
    try:
        credential = DefaultAzureCredential()

        key_vault_name = os.getenv("KEY_VAULT_NAME")
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

        global secret_client
        secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

        return secret_client
    except Exception as e:
        raise e


def get_secret(key):
    try:
        global secret_client
        if secret_client is None:
            secret_client = get_secret_client()

        value = secret_client.get_secret(key)
        value = str(value.value)
        return value
    except Exception as e:
        raise e
