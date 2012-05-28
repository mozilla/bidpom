#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class VerifyEmailAddress(Base):

    _email_locator = 'id=email'
    _password_locator = 'id=password'
    _verify_password_locator = 'id=vpassword'
    _finish_locator = 'css=div.submit > button'
    _thank_you_locator = 'id=congrats'

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.wait_for_element_visible(self._email_locator)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.get_text(self._email_locator)

    @property
    def password(self):
        """Get the value of the password field."""
        return self.selenium.get_text(self._password_locator)

    @password.setter
    def password(self, value):
        """Set the value of the password field."""
        self.selenium.type(self._password_locator, value)

    @property
    def verify_password(self):
        """Get the value of the password field."""
        return self.selenium.get_text(self._verify_password_locator)

    @password.setter
    def verify_password(self, value):
        """Set the value of the password field."""
        self.selenium.type(self._verify_password_locator, value)

    def click_finish(self):
        """Clicks the 'finish' button."""
        self.selenium.click(self._finish_locator)
        self.wait_for_element_visible(self._thank_you_locator)

    def verify_email_address(self, password):
        self.password = password
        self.verify_password = password
        self.click_finish()
