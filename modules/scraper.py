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

class Scraper(object):
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


    def get_users(self, group, target, link, verbose = False):
        f = open("output.txt", "a")
        """Return a list of links to the users profiles found."""

        if link is None:
            wblink = self._get_link(group, target)
            if wblink is None:
                return []
            self._open_dialog(wblink)
            if self.users_list_container is None:
                return None
        else:
            wblink = self._get_link_by_link(group, link)
            if wblink is None:
                return []
            self._open_dialog(wblink)
            if self.users_list_container is None:
                return None

        print('\nGetting {} users…{}'.format(
            self.expected_number,
            '\n' if verbose else ''
        ))

        links = []
        last_user_index = 0
        updated_list = self._get_updated_user_list()
        initial_scrolling_speed = 5
        retry = 2

        # While there are more users scroll and save the results
        while updated_list[last_user_index] is not updated_list[-1] or retry > 0:
            self._scroll(self.users_list_container, initial_scrolling_speed)

            for index, user in enumerate(updated_list):
                if index < last_user_index:
                    continue

                if index > 100:
                    return links

                try:
                    link_to_user = user.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    last_user_index = index
                    if link_to_user not in links:
                        links.append(link_to_user)
                        if verbose:
                            f.write(link_to_user + "\n")
                            print(
                                '{0:.2f} {1:s}'.format(
                                index,
                                link_to_user
                                )
                            )
                except:
                    if (initial_scrolling_speed > 1):
                        initial_scrolling_speed -= 1
                    pass

            updated_list = self._get_updated_user_list()
            if updated_list[last_user_index] is updated_list[-1]:
                retry -= 1

        f.close()
        print('100% Complete')
        return links


    def _open_dialog(self, link):
        """Open a specific dialog and identify the div containing the users
        list."""

        link.click()
        self.expected_number = int(
            re.search('(\d+)', link.text).group(1)
        )
        time.sleep(1)
        try:
            self.users_list_container = self.driver.find_element_by_xpath(
                '//div[@role="dialog"]//ul/parent::div'
            )
        except:
            self.users_list_container = None


    def _get_link(self, group, target):
        """Return the element linking to the users list dialog."""

        print('\nNavigating to %s profile…' % target)
        self.driver.get('https://www.instagram.com/%s/' % target)
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, group))
            )
        except:
            return None

    def _get_link_by_link(self, group, link):
        """Return the element linking to the users list dialog."""

        print('\nNavigating to %s profile…' % link)
        self.driver.get(link)
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, group))
            )
        except:
            return None


    def _get_updated_user_list(self):
        """Return all the list items included in the users list."""

        return self.users_list_container.find_elements(By.XPATH, 'ul//li')


    def _scroll(self, element, times = 1):
        """Scroll a specific element one or more times with small delay between
        them."""

        while times > 0:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight',
                element
            )
            time.sleep(random() * randint(2, 5))
            times -= 1
