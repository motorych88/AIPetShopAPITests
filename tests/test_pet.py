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
