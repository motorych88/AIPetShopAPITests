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
    assert response.status_code == 200, 'Статус код ответа неверный'
    return response_json


@pytest.fixture(scope="function")
def info_pet(create_pet):
    id_pet = create_pet["id"]
    response = requests.get(url=f'{BASE_URL}/pet/{id_pet}')
    response_json = response.status_code
    assert response.status_code == 404, 'Статус код ответа неверный'
    return response_json



# @pytest.fixture(scope="function")
# def delete_pet(create_pet):
#     response = requests.get(url=f'{BASE_URL}/pet/{create_pet["id"]}')
#     response_json = response.json()
#     assert response.status_code == 404, 'Статус код ответа неверный'
#     return response_json

