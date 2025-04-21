import pytest
import requests
from faker import Faker

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@pytest.fixture(scope="function")
def create_pet():
    faker = Faker()
    faker_id = faker.random_number()
    faker_id_tags = faker.random_number()
    faker_name = faker.first_name()
    faker_name_tags = faker.first_name()

    payload = {
        "id": faker_id,
        "name": faker_name,
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": faker_id_tags, "name": faker_name_tags}],
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}/pet', json=payload)
    response_json = response.json()
    yield response_json
    requests.delete(url=f'{BASE_URL}/pet/{faker_id}')


@pytest.fixture(scope="function")
def add_order():
    payload = {
        "id": 1,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
    response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
    response_json = response.json()
    return response_json


@pytest.fixture(scope="function")
def create_user():
    faker = Faker()
    faker_id = faker.random_number()
    faker_name = faker.first_name()
    faker_first_name = faker.first_name()
    faker_last_name = faker.last_name()
    faker_email = faker.email()
    faker_password = faker.password()
    faker_status = faker.random_number()

    payload = {
        "id": faker_id,
        "username": faker_name,
        "firstName": faker_first_name,
        "lastName": faker_last_name,
        "email": faker_email,
        "password": faker_password,
        "phone": "12345",
        "userStatus": faker_status
    }
    response = requests.post(url=f'{BASE_URL}/user', json=payload)
    response_json = response.json()
    yield response_json
    requests.delete(url=f'{BASE_URL}/pet/{faker_name}')
