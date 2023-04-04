import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Test 1 (Присутствуют все питомцы)
def test_all_pets(logging):
    score = WebDriverWait(logging, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.table.table-hover>tbody>tr')))
    count = 0
    for i in score:
        count += 1

    assert str(count) == logging.find_element(By.CSS_SELECTOR, 'div.\.col-sm-4.left').text.split('\n')[1].split(' ')[1]


# Test 2 (Хотя бы у половины питомцев есть фото)
def test_have_photo(logging):
    logging.implicitly_wait(10)
    score = logging.find_elements(By.CSS_SELECTOR, 'table.table.table-hover>tbody>tr>th>img')
    count = 0
    for i in range(len(score)):
        if score[i].get_attribute('src') != '':
            count += 1
    assert len(score)/count <= 2, 'Менее половины питомцев имеет фотографию'


# Test 3 (У всех питомцев есть имя, возраст и порода)
def test_pets_have_name_age_type(logging):
    logging.implicitly_wait(10)
    score = logging.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    for i in score:
        assert len(i.text.split(' ')) == 3, f'Один из 3 необходимых параметров: имя, возраст, порода отсутствует у элемента {i.text}'


# Test 4 (У всех питомцев разные имена)
def test_names_different(logging):
    logging.implicitly_wait(10)
    score = logging.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    list_names = []
    for i in score:
        list_names.append(i.text.split(' ')[0])
    assert len(list_names) == len(set(list_names)), 'Не у всех ваших питомцев разные имена, есть повторяющиеся'


# Test 5 (В списке нет повторяющихся питомцев)
def test_duplicated_pets(logging):
    logging.implicitly_wait(10)
    score = logging.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    list_names = []
    list_duplicated_pets = []
    for i in score:
        pet_attr = i.text.strip('\n×').split(' ')
        if pet_attr in list_names:
            list_duplicated_pets.append(pet_attr)
        else:
            list_names.append(pet_attr)
    assert len(list_duplicated_pets) == 0, 'В вашем списке есть повторяющиеся питомцы (имена, порода и возраст совпадают)'


