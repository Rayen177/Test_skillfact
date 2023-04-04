from selenium import webdriver
import pytest
from Exercise_25_5_1.config import valid_email, valid_password
from selenium.webdriver.common.by import By

@pytest.fixture(scope='session')
def logging():
    base_url = 'https://petfriends.skillfactory.ru'
    driver = webdriver.Chrome()
    driver.get(base_url)

    # нажатие кнопки Зарегистрироваться
    driver.implicitly_wait(10)
    reg_button = driver.find_element(By.XPATH, '//button[text()="Зарегистрироваться"]')
    reg_button.click()

    #Выбор условия - У меня уже есть аккаунт
    driver.find_element(By.LINK_TEXT, 'У меня уже есть аккаунт').click()

    #Заполнение полей для уже зарегистрированного пользователя
    email_field = driver.find_element(By.CSS_SELECTOR, 'input#email')
    email_field.send_keys(valid_email)
    password_field = driver.find_element(By.CSS_SELECTOR, 'input#pass')
    password_field.send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, '.btn.btn-success').click()

    #Переходим на страницу my_pets
    driver.find_element(By.LINK_TEXT , 'Мои питомцы').click()

    # вызов теста
    yield driver

    # закрываем сеанс
    driver.quit()
