import pytest
from rest_framework.test import APIRequestFactory

pytestmark = pytest.mark.django_db


def test_sync_empty():
    api_factory = APIRequestFactory()
    request = api_factory.post('/sync/', [])
    assert request is not None
