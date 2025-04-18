import pytest
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@pytest.fixture(scope="function")
def create_pet():
    payload = {
        "id": 800,
        "name": "Jackson",
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}/pet', json=payload)
    response_json = response.json()
    return response_json
