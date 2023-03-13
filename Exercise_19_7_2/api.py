import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """список запросов, поддерживаемых PetFriends REST API"""

    def __init__(self):
        # присвоение переменной базового URL PetFriends
        self.base_url = 'https://petfriends.skillfactory.ru'


    def get_api_key(self, email: str, password: str) -> json:
        '''GET api метод, выполняет запрос для получения авторизационного ключа в формате json.
        Вовращает статус запроса и ключ в json формате'''

        header = {
            'email': email,
            'password': password
        }
        response = requests.get(self.base_url + '/api/key', headers=header)

        status = response.status_code
        result = ''
        # проверка того, что полученый ответ можно представить в формате json
        try:
            result = response.json()
        except:
            result = response.text
        return status, result


    def get_list_pets(self, auth_key: json, filter: str = '') -> json:
        '''GET api метод, выполняет запрос для получения списка доступных животных. Может быть
        применен фильтр - my_pets, в этом случае получим список только из ваших животных.
        Возвращает статус и список животных в формате json'''

        header = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        response = requests.get(self.base_url + '/api/pets', headers=header, params=filter)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result


    def post_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """POST api метод, осуществляет добавление нового питомца с фотографией. возвращает данные
        добавленого питомца в фомате json"""

        data = MultipartEncoder(fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        header = {
            'auth_key': auth_key['key'],
            'Content-type': data.content_type
        }
        response = requests.post(self.base_url + '/api/pets', headers=header, data=data)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        '''DELETE api метод, который удаляет записи по предоставленному id'''
        header = {'auth_key': auth_key['key']}
        response = requests.delete(self.base_url + f'/api/pets/{pet_id}', headers=header)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result


    def put_update_info_pet(self, auth_key: json, name: str, animal_type: str, age: str,
                            pet_id: str) -> json:
        """PUT api метод, позволяет вносить изменения в имя, тип и возраст животного по предоставленному id.
        возвращает данные измененного питомца в фомате json"""
        header = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        response = requests.put(self.base_url + f'/api/pets/{pet_id}', headers=header, data=data)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result


    def post_create_pet_simple(self, auth_key: json, name: str, animal_type: str,
                               age: str) -> json:
        """POST api метод, осуществляет добавление нового питомца без фотографии. возвращает данные
        добавленого питомца в фомате json"""
        header = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        response = requests.post(self.base_url + '/api/create_pet_simple', headers=header, data=data)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result


    def post_add_photo(self, auth_key: json, pet_id: str, pet_photo: str):
        """POST api метод, осуществляет добавление фотографии для существующего питомца по его id.
         возвращает данные питомца в фомате json"""
        data = MultipartEncoder(fields={
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        header = {
            'auth_key': auth_key['key'],
            'Content-type': data.content_type
        }
        response = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=header,
                                 data=data)

        status = response.status_code
        result = ''
        try:
            result = response.json()
        except:
            result = response.text

        return status, result
