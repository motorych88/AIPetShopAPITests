from http.client import responses

import allure
import requests

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