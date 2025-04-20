import allure
import jsonschema
import pytest
import requests

from conftest import create_pet
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
    def test_add_full_payload_pet(self):
        with allure.step('Отправка запроса на добавление'):
            payload = {
                "id": 11,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 1, "name": "Bulldog"}],
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step('Проверка JSON ответа'):
            assert response_json["id"] == payload["id"], 'id тела не совпадает с id ответа'
            assert response_json["name"] == payload["name"], 'name в теле не совпадает с name в ответе'
            assert response_json["category"]["id"] == payload["category"]["id"]
            assert response_json["category"]["name"] == payload["category"]["name"]
            assert response_json["photoUrls"] == payload["photoUrls"]
            assert response_json["tags"][0]["id"] == payload["tags"][0]["id"]
            assert response_json["tags"][0]["name"] == payload["tags"][0]["name"]
            assert response_json["status"] == payload["status"], 'Status тела не совпадает с Status ответа'

    @allure.title('Получение информации по ID')
    def test_get_pet_id(self, create_pet):
        with allure.step('Получение ID питомца'):
            id_pet = create_pet["id"]
        with allure.step('Отправка запроса на получение информации'):
            response = requests.get(url=f'{BASE_URL}/pet/{id_pet}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Проверка JSON ответа'):
            assert response.json()["id"] == id_pet

    @allure.title('Обновление информации о питомце')
    def test_update_pet(self, create_pet):
        with allure.step('Получение ID питомца'):
            id_pet = create_pet["id"]
            payload = {
                "id": id_pet,
                "name": "Buddy Updated",
                "status": "sold"
            }
        with allure.step('Отправка запроса на обновление информации о питомце'):
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step('Проверка JSON ответа'):
            assert response_json["name"] != create_pet["name"], 'Имя питомца не изменилось'
            assert response_json["status"] != create_pet["status"], 'Статус не поменялся'
            assert response_json["id"] == payload["id"], 'id тела не совпадает с id ответа'
            assert response_json["name"] == payload["name"], 'Имя питомца не совпадает с именем в ответе'
            assert response_json["status"] == payload["status"], 'Status тела не совпадает с Status ответа'

    @allure.title('Удаление питомца')
    def test_delete_pet(self, create_pet):
        with allure.step('Получение ID питомца'):
            id_pet = create_pet["id"]
        with allure.step('Отправка запроса на удаление'):
            response = requests.delete(url=f'{BASE_URL}/pet/{id_pet}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'Pet deleted', 'Текст ответа неверный'
        with allure.step('Проверка что информации о питомце нет'):
            response_info = requests.get(url=f'{BASE_URL}/pet/{id_pet}')
            assert response_info.status_code == 404, 'Питомец не удален'

    @allure.title('Получение списка питомцев по статусу')
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ("ass", 400),
            ("", 400)
        ]
    )
    def test_get_pet_list_for_status(self, status, expected_status_code):
        with allure.step(f'Отправка запроса на получение питомцев по статусу {status}'):
            response = requests.get(url=f'{BASE_URL}/pet/findByStatus', params={"status": status})
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == expected_status_code, 'Статус код ответа неверный'
        with allure.step('Проверка формата данных ответа'):
            if response.status_code == 200:
                assert isinstance(response.json(), list), 'формат ответ не массив'
            elif response.status_code == 400:
                assert isinstance(response.json(), dict), 'формат ответа не объект'

    @allure.title('Получение списка питомцев по тэгу')
    def test_get_pet_list_for_tags(self, create_pet):
        tags = create_pet["tags"][0]["name"]
        with allure.step(f'Отправка запроса на получение питомцев по тэгу {tags}'):
            response = requests.get(url=f'{BASE_URL}/pet/findByTags', params={"tags": tags})
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            first_pet_response = response_json[0]
        with allure.step('Проверка статуса ответа'):
            assert first_pet_response["tags"][0]["name"] == create_pet["tags"][0]["name"]
            assert first_pet_response["tags"][0]["id"] == create_pet["tags"][0]["id"]

    @allure.title('Получение списка питомцев по несуществующему тэгу')
    @pytest.mark.parametrize(
        "tags, expected_status_code, expected_responce",
        [
            ("Ass", 200, []),
            ("", 400, 'No tags provided. Try again?')
        ]
    )
    def test_get_pet_list_for_tags(self, tags, expected_status_code, expected_responce):
        with allure.step(f'Отправка запроса на получение питомцев по тэгу {tags}'):
            response = requests.get(url=f'{BASE_URL}/pet/findByTags', params={"tags": tags})
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == expected_status_code, 'Статус код ответа неверный'
        with allure.step('Проверка формата данных ответа'):
            if expected_status_code == 200:
                assert response.json() == expected_responce, 'формат ответ не массив'
            elif expected_status_code == 400:
                assert response.text == expected_responce, 'Текст ответа неверный'
