import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client(katubi_user):
    """
    An API client with a valid user token.
    """
    # Create an auth token for the user.
    token, __ = Token.objects.get_or_create(user=katubi_user)

    # Create a client and attach the token.
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client
