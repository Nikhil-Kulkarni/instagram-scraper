import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import seed
from random import random
from random import randint
import json

class Profiler(object):
    """Able to start up a browser, to authenticate to Instagram and get
    followers and people following a specific user."""


    def __init__(self):
        self.driver = webdriver.Chrome('drivers/chromedriver2')


    def close(self):
        """Close the browser."""
        self.driver.close()


    def authenticate(self, username, password):
        """Log in to Instagram with the provided credentials."""

        print('\nLogging in…')
        self.driver.get('https://www.instagram.com')

        # Go to log in
        login_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Forgot password?'))
        )

        # Authenticate
        username_input = self.driver.find_element_by_xpath(
            '//input[@name="username"]'
        )
        password_input = self.driver.find_element_by_xpath(
            '//input[@name="password"]'
        )

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)


    def get_user_profile(self, username):
        print('\nNavigating to %s profile…' % username)
        self.driver.get('https://www.instagram.com/%s?__a=1' % username)
        content = self.driver.page_source
        content = self.driver.find_element_by_tag_name('pre').text
        parsed_json = json.loads(content)

        return parsed_json
