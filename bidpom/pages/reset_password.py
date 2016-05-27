# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By


class ResetPassword(Base):

    _create_new_password_locator = (By.ID, 'password')
    _verify_password_locator = (By.ID, 'vpassword')
    _finish_button_locator = (By.CSS_SELECTOR, '.submit button')
    _thank_you_locator = (By.ID, 'congrats')

    def wait_for_page_to_load(self):
        el = self.find_element(By.TAG_NAME, 'body')
        self.wait.until(lambda s: 'needs_password' in el.get_attribute('class'))
        return self

    @property
    def new_password(self):
        """Get the value of the new password field."""
        return self.find_element(*self._create_new_password_locator).get_attribute('value')

    @new_password.setter
    def new_password(self, value):
        """Set the value of the new password field."""
        password = self.find_element(*self._create_new_password_locator)
        password.clear()
        password.send_keys(value)

    @property
    def verify_password(self):
        """Get the value of the verify password field."""
        return self.find_element(*self._verify_password_locator).get_attribute('value')

    @verify_password.setter
    def verify_password(self, value):
        """Set the value of the verify password field."""
        password = self.find_element(*self._verify_password_locator)
        password.clear()
        password.send_keys(value)

    def click_finish(self):
        """Click finish"""
        self.find_element(*self._finish_button_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._thank_you_locator))

    @property
    def thank_you(self):
        """Returns the 'thank you' message."""
        return self.find_element(*self._thank_you_locator).text
