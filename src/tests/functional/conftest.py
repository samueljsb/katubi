import pytest


@pytest.fixture
def katubi_user(django_user_model):
    """
    A regular Django user.
    """
    return django_user_model.objects.create_user(
        username="username", password="password"
    )
