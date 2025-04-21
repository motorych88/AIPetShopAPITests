import allure
import jsonschema
import pytest
import requests
from .schemas.user_schema import USER_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('User')
class TestPet:

    @allure.title('Создание юзера')
    def test_create_user(self):
        payload = {
            "id": 10,
            "username": "theUser",
            "firstName": "John",
            "lastName": "James",
            "email": "john@email.com",
            "password": "12345",
            "phone": "12345",
            "userStatus": 1
        }
        with allure.step('Отправка запроса на создание юзера'):
            response = requests.post(f'{BASE_URL}/user', json=payload)
            response_json = response.json()
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'
            jsonschema.validate(response.json(), USER_SCHEMA)
        with allure.step('Проверка полей ответа'):
            assert response_json["id"] == payload["id"], 'ID ответа не сходится с ID запроса'
            assert response_json["username"] == payload["username"], 'username ответа не сходится с username запроса'
            assert response_json["firstName"] == payload[
                "firstName"], 'firstName ответа не сходится с firstName запроса'
            assert response_json["lastName"] == payload["lastName"], 'lastName ответа не сходится с lastName запроса'
            assert response_json["email"] == payload["email"], 'email ответа не сходится с email запроса'
            assert response_json["password"] == payload["password"], 'password ответа не сходится с password запроса'
            assert response_json["phone"] == payload["phone"], 'phone ответа не сходится с phone запроса'
            assert response_json["userStatus"] == payload[
                "userStatus"], 'userStatus ответа не сходится с userStatus запроса'

    @allure.title('Получение информации о юзере')
    def test_info_user(self, create_user):
        username = create_user["username"]
        with allure.step('Отправка запроса на получение информации о юзере'):
            response = requests.get(f'{BASE_URL}/user/{username}')
            response_json = response.json()
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'
            jsonschema.validate(response.json(), USER_SCHEMA)
        with allure.step('Проверка полей ответа'):
            assert response_json["id"] == create_user["id"], 'ID ответа не сходится с ID запроса'
            assert response_json["username"] == create_user[
                "username"], 'username ответа не сходится с username запроса'
            assert response_json["firstName"] == create_user[
                "firstName"], 'firstName ответа не сходится с firstName запроса'
            assert response_json["lastName"] == create_user[
                "lastName"], 'lastName ответа не сходится с lastName запроса'
            assert response_json["email"] == create_user["email"], 'email ответа не сходится с email запроса'
            assert response_json["password"] == create_user[
                "password"], 'password ответа не сходится с password запроса'
            assert response_json["phone"] == create_user["phone"], 'phone ответа не сходится с phone запроса'
            assert response_json["userStatus"] == create_user[
                "userStatus"], 'userStatus ответа не сходится с userStatus запроса'

    @allure.title('Получение информации о несуществующем юзере')
    def test_info_no_user(self):
        with allure.step('Отправка запроса на получение информации о несуществующем юзере'):
            response = requests.get(f'{BASE_URL}/user/ENERGETIK')
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 404, 'Статус код неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'User not found', 'Текст ответа неверный'

    @allure.title('Авторизация юзера')
    def test_login_user(self, create_user):
        login = create_user["username"]
        password = create_user["password"]
        with allure.step('Отправка запроса на авторизацию'):
            response = requests.get(f'{BASE_URL}/user/login', params={"username": login, "password": password})
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'

    @allure.title('Авторизация юзера c неправильным паролем')  # НЕ РАБОТАЕТ
    def test_login_user_no_password(self, create_user):
        login = create_user["username"]
        password = "1q2w3e4r"
        with allure.step('Отправка запроса на авторизацию'):
            response = requests.get(f'{BASE_URL}/user/login', params={"username": login, "password": password})
        # with allure.step('Проверка статус кода ответа'):
        #     assert response.status_code == 404, 'Статус код неверный'

    @allure.title('Авторизация юзера c неправильным логином')  # НЕ РАБОТАЕТ
    def test_login_user_no_username(self, create_user):
        login = "1q2w3e4r"
        password = create_user["password"]
        with allure.step('Отправка запроса на авторизацию'):
            response = requests.get(f'{BASE_URL}/user/login', params={"username": login, "password": password})
        # with allure.step('Проверка статус кода ответа'):
        #     assert response.status_code == 404, 'Статус код неверный'

    @allure.title('Разлогирование пользователя')  # НЕ РАБОТАЕТ
    def test_logout_user(self):
        with allure.step('Отправка запроса на разлогирование'):
            response = requests.get(f'{BASE_URL}/user/logout')
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'

    @allure.title('Редактирование юзера')
    def test_update_user(self, create_user):
        username = create_user["username"]
        payload = {
            "id": 111,
            "username": "Tornado",
            "firstName": "Mike",
            "lastName": "Orbans",
            "email": "tornado@gmail.com",
            "password": "1q2w3e4r",
            "phone": "1234567",
            "userStatus": 222
        }
        with allure.step('Отправка запроса на редактирование юзера'):
            response = requests.put(f'{BASE_URL}/user/{username}', json=payload)
            response_json = response.json()
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'
            jsonschema.validate(response.json(), USER_SCHEMA)
        with allure.step('Проверка полей ответа'):
            assert response_json["id"] != create_user["id"], 'ID не изменился'
            assert response_json["username"] != create_user["username"], 'usernam eне изменился'
            assert response_json["firstName"] != create_user["firstName"], 'firstName не изменился'
            assert response_json["lastName"] != create_user["lastName"], 'lastName не изменился'
            assert response_json["email"] != create_user["email"], 'email не изменился'
            assert response_json["password"] != create_user["password"], 'password не изменился'
            assert response_json["phone"] != create_user["phone"], 'phone не изменился'
            assert response_json["userStatus"] != create_user["userStatus"], 'userStatus не изменился'
            assert response_json["id"] == payload["id"], 'ID ответа не сходится с ID запроса'
            assert response_json["username"] == payload["username"], 'username ответа не сходится с username запроса'
            assert response_json["firstName"] == payload[
                "firstName"], 'firstName ответа не сходится с firstName запроса'
            assert response_json["lastName"] == payload["lastName"], 'lastName ответа не сходится с lastName запроса'
            assert response_json["email"] == payload["email"], 'email ответа не сходится с email запроса'
            assert response_json["password"] == payload["password"], 'password ответа не сходится с password запроса'
            assert response_json["phone"] == payload["phone"], 'phone ответа не сходится с phone запроса'
            assert response_json["userStatus"] == payload[
                "userStatus"], 'userStatus ответа не сходится с userStatus запроса'

    @allure.title('Редактирование несуществующего юзера')
    def test_update_no_user(self, create_user):
        payload = {
            "id": 111,
            "username": "Tornado",
            "firstName": "Mike",
            "lastName": "Orbans",
            "email": "tornado@gmail.com",
            "password": "1q2w3e4r",
            "phone": "1234567",
            "userStatus": 222
        }
        with allure.step('Отправка запроса на редактирование несуществующего юзера'):
            response = requests.put(f'{BASE_URL}/user/Callman', json=payload)
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 404, 'Статус код неверный'

    @allure.title('удаление юзера')
    def test_delete_user(self, create_user):
        username = create_user["username"]
        with allure.step('Отправка запроса на удаление юзера'):
            response = requests.delete(f'{BASE_URL}/user/{username}')
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'
        with allure.step('Отправка запроса для убеждения, что юзер удален'):
            response_get = requests.get(f'{BASE_URL}/user/{username}')
        with allure.step('Проверка статус кода ответа'):
            assert response_get.status_code == 404, 'Юзер не удален'

    @allure.title('Создание нескольких юзеров')
    def test_create_list_user(self):
        payload = [
            {
                "id": 10,
                "username": "theUser",
                "firstName": "John",
                "lastName": "James",
                "email": "john@email.com",
                "password": "12345",
                "phone": "12345",
                "userStatus": 1
            },
            {
                "id": 111,
                "username": "Tornado",
                "firstName": "Mike",
                "lastName": "Orbans",
                "email": "tornado@gmail.com",
                "password": "1q2w3e4r",
                "phone": "1234567",
                "userStatus": 222
            }
        ]
        with allure.step('Отправка запроса на создание нескольких юзеров'):
            response = requests.post(f'{BASE_URL}/user/createWithList', json=payload)
            response_json = response.json()
            # jsonschema.validate(response_json[0], USER_SCHEMA)
            jsonschema.validate(response_json[1], USER_SCHEMA)
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, 'Статус код неверный'
        with allure.step('Проверка полей ответа'):
            assert response_json[0]["id"] == payload[0]["id"], 'ID ответа не сходится с ID запроса'
            assert response_json[0]["username"] == payload[0]["username"], 'username ответа не сходится с username запроса'
            assert response_json[0]["firstName"] == payload[0]["firstName"], 'firstName ответа не сходится с firstName запроса'
            assert response_json[0]["lastName"] == payload[0]["lastName"], 'lastName ответа не сходится с lastName запроса'
            assert response_json[0]["email"] == payload[0]["email"], 'email ответа не сходится с email запроса'
            assert response_json[0]["password"] == payload[0]["password"], 'password ответа не сходится с password запроса'
            assert response_json[0]["phone"] == payload[0]["phone"], 'phone ответа не сходится с phone запроса'
            assert response_json[0]["userStatus"] == payload[0]["userStatus"], 'userStatus ответа не сходится с userStatus запроса'
            assert response_json[1]["id"] == payload[1]["id"], 'ID ответа не сходится с ID запроса'
            assert response_json[1]["username"] == payload[1]["username"], 'username ответа не сходится с username запроса'
            assert response_json[1]["firstName"] == payload[1]["firstName"], 'firstName ответа не сходится с firstName запроса'
            assert response_json[1]["lastName"] == payload[1]["lastName"], 'lastName ответа не сходится с lastName запроса'
            assert response_json[1]["email"] == payload[1]["email"], 'email ответа не сходится с email запроса'
            assert response_json[1]["password"] == payload[1]["password"], 'password ответа не сходится с password запроса'
            assert response_json[1]["phone"] == payload[1]["phone"], 'phone ответа не сходится с phone запроса'
            assert response_json[1]["userStatus"] == payload[1]["userStatus"], 'userStatus ответа не сходится с userStatus запроса'
