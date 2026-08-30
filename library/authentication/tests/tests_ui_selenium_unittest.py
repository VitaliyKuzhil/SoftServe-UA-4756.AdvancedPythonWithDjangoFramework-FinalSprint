from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth import get_user_model
from authentication.tests.test_constants import *

CustomUser = get_user_model()



class LoginLogoutTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(time_to_wait=TIME_TO_WAIT)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass() 


    def setUp(self):
        self.driver.delete_all_cookies()

        self.user = CustomUser.objects.create_user(email=VALID_USER_EMAIL, 
                                                  password=VALID_USER_PASSWORD)
        self.user.is_active = True
        self.user.save()

        self.driver.get(self.live_server_url)


    def login_action(self, email, password):
        self.driver.find_element(By.ID, 'login').click()

        input_email_field = self.driver.find_element(By.NAME, 'email')
        input_email_field.send_keys(email)
        
        input_password_field = self.driver.find_element(By.NAME, 'password')
        input_password_field.send_keys(password)

        self.driver.find_element(By.CSS_SELECTOR, '[data-test-id=\'login-submit-btn\']').click()

        WebDriverWait(self.driver, timeout=TIME_TO_WAIT)


    def test_login_valid_user(self):
        self.login_action(VALID_USER_EMAIL, VALID_USER_PASSWORD)

        logout = self.driver.find_element(By.ID, 'logout')

        self.assertTrue(logout.is_displayed())
        self.assertIn(VALID_USER_EMAIL, self.driver.page_source)


    def test_logout_user(self):
        self.login_action(VALID_USER_EMAIL, VALID_USER_PASSWORD)

        self.driver.find_element(By.ID, 'logout').click()

        WebDriverWait(self.driver, timeout=TIME_TO_WAIT)

        register = self.driver.find_element(By.ID, 'register')
        login = self.driver.find_element(By.ID, 'login')

        self.assertTrue(register.is_displayed(), login.is_displayed())
        self.assertNotIn(VALID_USER_EMAIL, self.driver.page_source)


    def test_login_valid_user_with_invalid_password(self):
        self.login_action(VALID_USER_EMAIL, VALID_USER_INVALID_PASSWORD)

        error_message = self.driver.find_element(By.CLASS_NAME, 'error-message')

        self.assertTrue(error_message.is_displayed())

        self.assertIn("Enter a correct email and password.", error_message.text)


    def test_login_invalid_user(self):
        self.login_action(INVALID_USER_EMAIL, INVALID_USER_PASSWORD)

        error_message = self.driver.find_element(By.CLASS_NAME, 'error-message')

        self.assertTrue(error_message.is_displayed())

        self.assertIn("Enter a correct email and password.", error_message.text)
