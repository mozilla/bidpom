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

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._email_locator).is_displayed())

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

    def click_next(self):
        """Clicks the 'next' button."""
        self.selenium.find_element(*self._next_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
            lambda s: s.find_element(*self._password_locator).is_displayed())

    def click_sign_in(self):
        """Clicks the 'Sign In' button."""
        self.selenium.find_element(*self._sign_in_locator).click()
        self.selenium.switch_to_window('')

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next()
        self.password = password
        self.click_sign_in()
