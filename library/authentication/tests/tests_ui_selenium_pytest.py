import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth import get_user_model
from authentication.tests.test_constants import *


CustomUser = get_user_model()


@pytest.fixture(scope="module")
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()

    yield browser

    browser.quit()


@pytest.fixture(autouse=True)
def create_test_user():
    test_user = CustomUser.objects.create_user(email=VALID_USER_EMAIL,
                                               password=VALID_USER_PASSWORD)
    test_user.is_active = True
    test_user.save()

    return test_user


def login_action(driver, email, password):
    driver.find_element(By.ID, 'login').click()

    input_email_field = driver.find_element(By.NAME, 'email')
    input_email_field.send_keys(email)
    
    input_password_field = driver.find_element(By.NAME, 'password')
    input_password_field.send_keys(password)

    driver.find_element(By.CSS_SELECTOR, '[data-test-id=\'login-submit-btn\']').click()

    WebDriverWait(driver, timeout=TIME_TO_WAIT)


@pytest.mark.django_db
def test_login_valid_user(driver, live_server):
    driver.delete_all_cookies()
    driver.get(live_server.url)

    login_action(driver, VALID_USER_EMAIL, VALID_USER_PASSWORD)

    driver.implicitly_wait(time_to_wait=TIME_TO_WAIT)

    logout = driver.find_element(By.ID, 'logout')

    assert logout.is_displayed()
    assert VALID_USER_EMAIL in driver.page_source


@pytest.mark.django_db
def test_logout_user(driver, live_server):
    driver.delete_all_cookies()
    driver.get(live_server.url)

    login_action(driver, VALID_USER_EMAIL, VALID_USER_PASSWORD)

    driver.implicitly_wait(time_to_wait=TIME_TO_WAIT)

    driver.find_element(By.ID, 'logout').click()


    register = driver.find_element(By.ID, 'register')
    login = driver.find_element(By.ID, 'login')

    assert register.is_displayed()
    assert login.is_displayed()
    assert VALID_USER_EMAIL not in driver.page_source



@pytest.mark.django_db
def test_login_valid_user_with_invalid_password(driver, live_server):
    driver.delete_all_cookies()
    driver.get(live_server.url)

    login_action(driver, VALID_USER_EMAIL, VALID_USER_INVALID_PASSWORD)

    error_message = driver.find_element(By.CLASS_NAME, 'error-message')

    assert error_message.is_displayed()
    assert "Enter a correct email and password." == error_message.text


@pytest.mark.django_db
def test_login_invalid_user(driver, live_server):
    driver.delete_all_cookies()
    driver.get(live_server.url)

    login_action(driver, INVALID_USER_EMAIL, INVALID_USER_PASSWORD)
    driver.implicitly_wait(time_to_wait=TIME_TO_WAIT)

    error_message = driver.find_element(By.CLASS_NAME, 'error-message')

    assert error_message.is_displayed()
    assert "Enter a correct email and password." == error_message.text
