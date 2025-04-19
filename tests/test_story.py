import allure
import jsonschema
import pytest
import requests
from conftest import add_order

from tests.schemas.order_schema import ORDER_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Story')
class TestStory:

    @allure.title('Размещение заказа')
    def test_add_order(self):
        payload = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": "placed",
            "complete": True
        }
        with allure.step('Отправка запроса на размещение заказа'):
            response = requests.post(f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
            jsonschema.validate(response_json, ORDER_SCHEMA)
        with allure.step('Проверка JSON ответа'):
            assert response_json["id"] == payload["id"], 'ID ответа не совпадает с id запроса'
            assert response_json["petId"] == payload["petId"], 'petId ответа не совпадает с petId запроса'
            assert response_json["quantity"] == payload["quantity"], 'quantity ответа не совпадает с quantity запроса'
            assert response_json["status"] == payload["status"], 'status ответа не совпадает с status запроса'
            assert response_json["complete"] == payload["complete"], 'complete ответа не совпадает с complete запроса'

    @allure.title('Получение информации о заказе по ID')
    def test_get_order_by_id(self, add_order):
        order_id = add_order["id"]
        with allure.step('Отправка запроса на получение информации о заказе по ID'):
            response = requests.get(f'{BASE_URL}/store/order/{order_id}')
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Проверка JSON ответа'):
            assert response_json["id"] == add_order["id"], 'ID ответа не совпадает с id запроса'
            assert response_json["petId"] == add_order["petId"], 'petId ответа не совпадает с petId запроса'
            assert response_json["quantity"] == add_order["quantity"], 'quantity ответа не совпадает с quantity запроса'
            assert response_json["status"] == add_order["status"], 'status ответа не совпадает с status запроса'
            assert response_json["complete"] == add_order["complete"], 'complete ответа не совпадает с complete запроса'

    @allure.title('Удаление заказа по ID')
    def test_deleted_order_by_id(self, add_order):
        order_id = add_order["id"]
        with allure.step('Отправка запроса на удаление заказа по ID'):
            response = requests.delete(f'{BASE_URL}/store/order/{order_id}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Отправка запроса на получение информации о заказе по ID'):
            response_get = requests.get(f'{BASE_URL}/store/order/{order_id}')
        with allure.step('Проверка статуса ответа'):
            assert response_get.status_code == 404, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response_get.text == 'Order not found', 'Текст ответа неверный'

    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_get_nonexistent_order_by_id(self):
        with allure.step('Отправка запроса на получение несуществующем заказе по ID'):
            response = requests.get(f'{BASE_URL}/store/order/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Статус код ответа неверный'
        with allure.step('Проверка текста ответа'):
            assert response.text == 'Order not found', 'Текст ответа неверный'

    @allure.title('Получение инвентаря магазина')
    def test_get_inventory(self):
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = requests.get(f'{BASE_URL}/store/inventory')
            response_json = response.json()
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Статус код ответа неверный'
        with allure.step('Проверка JSON ответа'):
            assert response_json["approved"] == 57, 'количество approved неверное'
            assert response_json["available"] == 0, 'количество available неверное'
            assert response_json["delivered"] == 50, 'количество delivered неверное'