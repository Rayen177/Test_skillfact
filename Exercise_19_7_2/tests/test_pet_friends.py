import os
import random
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import string


class TestPFapi:
    def setup_method(self):
        # Создаем объект класса PetFriends
        self.obj = PetFriends()

    # Test_1
    def test_get_api_key_valid_email_valid_password_pass(self, email=valid_email, password=valid_password):
        '''Позитивная проверка, правильный email и правильный password. Проверяется статус запроса
         и то, что ответ содержит "key" '''

        status, result = self.obj.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    # Test_2
    def test_get_api_key_invalid_email_valid_password_fail(self, email=invalid_email,password=valid_password):
        '''Негативная проверка, с неправильным email и правильным password. Проверяется статус запроса
         и что ответ не содержит "key" '''

        status, result = self.obj.get_api_key(email, password)
        assert status == 403
        assert 'key' not in result

    # Test_3
    def test_get_api_key_valid_email_invalid_password_fail(self, email=valid_email,password=invalid_password):
        '''Негативная проверка, с правильным email и неправильным password. Проверяется статус запроса
         и то, что ответ не содержит "key" '''

        status, result = self.obj.get_api_key(email, password)
        assert status == 403
        assert 'key' not in result

    # Test_4
    def test_get_list_pets_valid_data_pass(self, email=valid_email, password=valid_password, filter=''):
        """Позитивная проверка, с правильным email и правильным password. Проверяется статус запроса
         и что ответ не пустой лист '''"""

        _, auth_key = self.obj.get_api_key(email, password)
        status, result = self.obj.get_list_pets(auth_key, filter)

        assert status == 200
        assert len(result['pets']) > 0

    # Test_5
    def test_get_list_pets_invalid_filter_fail(self, email=valid_email, password=valid_password, filter='chukka'):
        """Негативная проверка, с правильным email и правильным password, но с неправильным значением фильтра.
         Допустимое значение фильтра - my_pets. Проверяется статус запроса"""

        _, auth_key = self.obj.get_api_key(email, password)
        status, result = self.obj.get_list_pets(auth_key, filter)

        assert status == 500

    # Test_6
    def test_post_new_pet_valid_data_pass(self, name='Melisa', animal_type='Koshara', age='12',
                               pet_photo='images\koshka.jpeg'):
        """Позитивная проверка, все входные данные: name, animal_type, age, pet_photo корректны.
        Проверяется статус запроса, совпадение имени в созданной карточке с тем что было подано на вход,
        а так же что фотография питомца присутствует"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        status, result = self.obj.post_new_pet(auth_key, name, animal_type, age, pet_photo)

        assert status == 200
        assert result['name'] == name
        assert len(result['pet_photo']) > 0

    # Test_7
    def test_post_new_pet_invalid_photo_fail(self, name='Melisa', animal_type='Koshara', age='12',
                                          pet_photo=''):
        """Негативная проверка, все входные данные: name, animal_type, age корректны за исключением pet_photo,
         имя файла не указано. Проверяется путь до файла с фото, если путь существует выполняется обычная проверка,
         а если файла не существует позитивный тест не запускается"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        try:
            status, result = self.obj.post_new_pet(auth_key, name, animal_type, age, pet_photo)
        except FileNotFoundError:
            print()
            print(f'Указаного файла "{pet_photo}" не существует')
            assert not os.path.isfile(pet_photo)
        else:
            assert status == 200
            assert result['name'] == name
            assert len(result['pet_photo']) > 0

    # Test_8
    def test_delete_pet_valid_key_pass(self):
        """Позитивная проверка, удаление существующей записи с правильным авторизационным ключом """
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')

        if len(my_pets['pets']) == 0:
            self.obj.post_new_pet(name='Melisa', animal_type='Koshara', age='12',
                                  pet_photo='images\koshka.jpeg')
            _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')

        pet_id = my_pets['pets'][0]['id']

        status, _ = self.obj.delete_pet(auth_key, pet_id)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')

        assert status == 200
        assert pet_id not in my_pets.values()

    # Test_9
    def test_delete_pet_invalid_key_fail(self):
        """Негативная проверка, удаление существующей записи с неправильным авторизационным ключом """
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')
        # подмена правильного ключа на неправильный
        auth_key = {'key': 'bb7aefdce7f0264680d0d36577c885a0d1b6b44ec4490ffeeb9dadb4'}
        if len(my_pets['pets']) == 0:
            self.obj.post_new_pet(name='Melisa', animal_type='Koshara', age='12',
                                  pet_photo='images\koshka.jpeg')
            _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')

        pet_id = my_pets['pets'][0]['id']

        status, _ = self.obj.delete_pet(auth_key, pet_id)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')

        assert status == 403

    # Test_10
    def test_delete_pet_invalid_id_fail(self):
        """Негативная проверка, удаление записи по id не принадлежащая мне """
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')
        _, all_pets = self.obj.get_list_pets(auth_key, filter='')

        all_id = [all_pets['pets'][i]['id'] for i in range(len(all_pets['pets']))]
        my_id = [my_pets['pets'][i]['id'] for i in range(len(my_pets['pets']))]

        pet_id = random.choice([i for i in all_id if i not in my_id])

        status, _ = self.obj.delete_pet(auth_key, pet_id)
        _, all_pets = self.obj.get_list_pets(auth_key, filter='')

        assert status == 200
        assert pet_id not in all_pets.values()


    # Test_11
    def test_put_update_info_pet_valid_data_pass(self, name='Kalosha', animal_type='Koshara', age='14'):
        """Позитивный тест, изменение данных в существующей карточке питомца с правильными данными"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, result = self.obj.put_update_info_pet(auth_key, name, animal_type, age, pet_id)

            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("Your list of pets is empty")

    # Test_12
    def test_put_update_info_pet_invalid_age_fail(self, name='Kalosha', animal_type='Koshara', age=-25):
        """Негативный тест, изменение данных в существующей карточке питомца, передаем отрицательный возраст"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, result = self.obj.put_update_info_pet(auth_key, name, animal_type, age,
                                                          pet_id)

            assert status == 200
            assert int(result['age']) < 0
        else:
            raise Exception("Your list of pets is empty")

    # Test_13
    def test_post_create_pet_simple_valid_data_pass(self, name='Teodor', animal_type='Doggy', age='5'):
        """Позитивный тест, создание новой карточки с правильными данными"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        status, result = self.obj.post_create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    # Test_14
    def test_post_create_pet_simple_invalid_name_fail(self, name='TeodorTeodorTeodorTeodorTeodor1', animal_type='Doggy', age='5'):
        """Негативный тест, создание новой карточки с неправильным именем, длина имени больше 30 символов"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        status, result = self.obj.post_create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert 30 < len(result['name']) or len(result['name']) < 1

    # Test_15
    def test_post_create_pet_simple_invalid_animal_type_fail(self, name='Teodor', animal_type='D%og>gy', age='5'):
        """Негативный тест, создание новой карточки с неправильным форматом типа животного, применение спец символов в имени типа"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)

        status, result = self.obj.post_create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        out_symbols = [i for i in list(string.punctuation) if i in animal_type]
        assert len(out_symbols) > 0

    # Test_16
    def test_post_create_pet_simple_invalid_big_age_fail(self, name='Teodor', animal_type='Doggy', age='55'):
        """Негативный тест, создание новой карточки с большим значением возраста , ограничение на возраст - 30 лет"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)

        status, result = self.obj.post_create_pet_simple(auth_key, name, animal_type, age)

        assert status == 200
        assert int(result['age']) > 30

    # Test_17
    def test_post_add_photo_pass(self, pet_photo='images\korgi.jpeg'):
        """Позитивный тест, правильные авторизационные данные, правильное имя файла"""
        _, auth_key = self.obj.get_api_key(valid_email, valid_password)
        _, my_pets = self.obj.get_list_pets(auth_key, filter='my_pets')
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        if len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, result = self.obj.post_add_photo(auth_key, pet_id, pet_photo)

            assert status == 200
            assert len(result['pet_photo']) > 0

        else:
            raise Exception("Your list of pets is empty")

