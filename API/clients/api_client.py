import requests, json
from API.config import BASE_URL


class APIClient:
    def __init__(self,base_url):
        self.base_url = BASE_URL

    def get(self, endpoint, headers=None):
        return requests.get(f"{self.base_url}{endpoint}", headers=headers)

    def post(self, endpoint, data=None, headers=None):
        return requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)

    def put(self, endpoint, data=None, headers=None):
        return requests.put(f"{self.base_url}{endpoint}", json=data, headers=headers)

    def delete(self, endpoint, headers=None):
        return requests.delete(f"{self.base_url}{endpoint}", headers=headers)
