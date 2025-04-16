from http.client import responses

import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Pet')
class TestPet:

    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_nonexistent_pet(self):
        with allure.step('Отправка запроса на удаление'):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'Pet deleted', 'Текст ответа неверный'

    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_nonexistent_pet(self):
        with allure.step('Отправка запроса на обновление'):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'Pet not found', 'Текст ответа неверный'

    @allure.title('Попытка получить информацию о несуществующем питомце')
    def test_update_nonexistent_pet(self):
        with allure.step('Отправка запроса на получение информации'):
            response = requests.get(url=f'{BASE_URL}/pet/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'Pet not found', 'Текст ответа неверный'

    @allure.title('Добавление нового питомца')
    def test_add_pet(self):
        with allure.step('Отправка запроса на добавление'):
            payload = {
                "id": 800,
                "name": "Jackson",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step('Проверка JSON ответа'):
            assert response_json["id"] == payload["id"]
            assert response_json["name"] == payload["name"]
            assert response_json["status"] == payload["status"]

    @allure.title('Добавление нового питомца c полным телом')
    def test_add_fullpayload_pet(self):
        with allure.step('Отправка запроса на добавление'):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step('Проверка JSON ответа'):
            assert response_json["id"] == payload["id"], 'id тела не совпадает с id ответа'
            assert response_json["name"] == payload["name"]
            assert response_json["category"]["id"] == payload["category"]["id"]
            assert response_json["category"]["name"] == payload["category"]["name"]
            assert response_json["photoUrls"] == payload["photoUrls"]
            assert response_json["tags"][0]["id"] == payload["tags"][0]["id"]
            assert response_json["tags"][0]["name"] == payload["tags"][0]["name"]
            assert response_json["status"] == payload["status"]