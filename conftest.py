import pytest
from API.config import BASE_URL
from API.clients.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient(BASE_URL)

@pytest.fixture
def context():
    return {}
