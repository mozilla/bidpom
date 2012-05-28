#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class SignIn(Base):

    _email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'password')
    _next_locator = (By.CSS_SELECTOR, 'button.start')
    _sign_in_locator = (By.CSS_SELECTOR, 'button.returning')
    _sign_in_returning_user_locator = (By.ID, 'signInButton')
    _verify_email_locator = (By.CSS_SELECTOR, 'button.newuser')
    _use_another_email_address_locator = (By.ID, 'back')

    def __init__(self, selenium, timeout, expect='new'):
        Base.__init__(self, selenium, timeout)

        if self.selenium.title != self._page_title:
            for handle in self.selenium.window_handles:
                self.selenium.switch_to_window(handle)
                if self.selenium.title == self._page_title:
                    break

        if expect == 'new':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*self._email_locator).is_displayed())
        elif expect == 'returning':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._sign_in_returning_user_locator).is_displayed())
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def close_window(self):
        self.selenium.close()

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.find_element(*self._email_locator).text

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = self.selenium.find_element(*self._email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def password(self):
        """Get the value of the password field."""
        return self.selenium.find_element(*self._password_locator).text

    @password.setter
    def password(self, value):
        """Set the value of the password field."""
        password = self.selenium.find_element(*self._password_locator)
        password.clear()
        password.send_keys(value)

    def click_next(self, expect='password'):
        """Clicks the 'next' button."""
        self.selenium.find_element(*self._next_locator).click()
        if expect == 'password':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._password_locator).is_displayed())
        elif expect == 'verify':
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(
                    *self._verify_email_locator).is_displayed())
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_sign_in(self):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(*self._sign_in_locator).click()
        self.switch_to_main_window()

    def click_sign_in_returning_user(self):
        """Clicks the 'sign in' button."""
        self.selenium.find_element(
            *self._sign_in_returning_user_locator).click()
        self.switch_to_main_window()

    def click_verify_email(self):
        """Clicks 'verify email' button."""
        self.selenium.find_element(*self._verify_email_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(
                *self._use_another_email_address_locator).is_displayed())

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next(expect='password')
        self.password = password
        self.click_sign_in()

    def sign_in_new_user(self, email):
        """Requests verification email using the specified email address."""
        self.email = email
        self.click_next(expect='verify')
        self.click_verify_email()
        self.close_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self):
        """Signs in with the stored user."""
        self.click_sign_in_returning_user()
