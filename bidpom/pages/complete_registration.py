# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By


class CompleteRegistration(Base):

    _email_locator = (By.ID, 'authentication_email')
    _password_locator = (By.ID, 'authentication_password')
    _finish_locator = (By.CSS_SELECTOR, 'div.submit > button')
    _user_loggedin_locator = (By.CSS_SELECTOR, '#loggedin span')

    def __init__(self, selenium, timeout=10, expect='success'):
        super(CompleteRegistration, self).__init__(selenium, timeout)

        if expect == 'success':
            self.wait.until(lambda s: self.is_element_displayed(
                *self._user_loggedin_locator))
        elif expect == 'verify':
            self.wait.until(lambda s: self.is_element_displayed(
                *self._password_locator))
        else:
            raise Exception('Unknown expect value: %s' % expect)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.find_element(*self._email_locator).text

    @property
    def password(self):
        """Get the value of the password field."""
        return self.find_element(*self._password_locator).text

    @password.setter
    def password(self, value):
        """Set the value of the password field."""
        password = self.find_element(*self._password_locator)
        password.clear()
        password.send_keys(value)

    def click_finish(self):
        """Clicks the 'finish' button."""
        self.find_element(*self._finish_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._thank_you_locator))

    @property
    def user_loggedin(self):
        """Returns the 'thank you' message."""
        return self.find_element(*self._user_loggedin_locator).text
