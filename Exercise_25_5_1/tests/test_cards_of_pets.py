import pytest
from config import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


@pytest.fixture(scope='session', autouse=True)
def logging():
    base_url = 'https://petfriends.skillfactory.ru'
    pytest.driver = webdriver.Chrome()
    pytest.driver.get(base_url)


    # нажатие кнопки Зарегистрироваться
    pytest.driver.implicitly_wait(10)
    reg_button = pytest.driver.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    reg_button.click()

    #Выбор условия - У меня уже есть аккаунт
    pytest.driver.find_element(By.LINK_TEXT, 'У меня уже есть аккаунт').click()

    #Заполнение полей для уже зарегистрированного пользователя
    email_field = pytest.driver.find_element(By.CSS_SELECTOR, 'input#email')
    email_field.send_keys(valid_email)
    password_field = pytest.driver.find_element(By.CSS_SELECTOR, 'input#pass')
    password_field.send_keys(valid_password)
    pytest.driver.find_element(By.CSS_SELECTOR, '.btn.btn-success').click()

    #Переходим на страницу my_pets
    pytest.driver.find_element(By.LINK_TEXT , 'Мои питомцы').click()


    yield

    pytest.driver.quit()

def test_all_pets():
    score = pytest.driver.find_elements(By.CSS_SELECTOR, 'table.table.table-hover>tbody>tr')
    count = 0
    for i in score:
        count += 1

    assert str(count) == pytest.driver.find_element(By.CSS_SELECTOR, 'div.\.col-sm-4.left').text.split('\n')[1].split(' ')[1]

def test_find_header():
    header = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar.navbar-expand-lg.navbar-light.bg-light'))
    )
    assert header

def test_logo_header():
    logo = WebDriverWait(pytest.driver, 5).until(
        EC.text_to_be_present_in_element((By.XPATH, "//a[@href='/']"), text_='PetFriends')
    )
    assert logo

def test_quit_button():

    quit_but = WebDriverWait(pytest.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[onclick="document.location=\'/logout\';"]'))
                                   )
    assert quit_but

def test_header_of_page():
    header_of_page = WebDriverWait(pytest.driver, 5).until(EC.text_to_be_present_in_element(
        (By.XPATH, "//h1[text() ='PetFriends']"), text_='PetFriends'))
    assert header_of_page


def test_card_of_pet():
    card_of_pet = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.card:nth-child(1)")))
    assert card_of_pet

def test_photo_of_pet():
    photo_of_pet = WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.card:nth-child(1)>div>img")))
    assert photo_of_pet

def test_name_of_pet():
    name_of_pet = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.card:nth-child(1) h5.card-title")))
    name = pytest.driver.find_element(By.CSS_SELECTOR, "div.card:nth-child(1) h5.card-title").text
    assert name is not None

def test_age_of_pet():
    name_of_pet = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.card:nth-child(1) p.card-text")))
    age = pytest.driver.find_element(By.CSS_SELECTOR, "div.card:nth-child(1) p.card-text").text.split(', ')
    assert age is not None



