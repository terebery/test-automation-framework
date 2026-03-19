import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.service import Service
from API.config import BASE_URL
from API.clients.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient(BASE_URL)

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    yield driver
    driver.quit()

@pytest.fixture
def context():
    return {}
