#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base


class CompleteRegistration(Base):

    _email_locator = 'id=email'
    _password_locator = 'id=password'
    _finish_locator = 'css=div.submit > button'
    _thank_you_locator = 'id=congrats'

    def __init__(self, selenium, timeout, expect='success'):
        Base.__init__(self, selenium, timeout)

        if expect == 'success':
            self.wait_for_element_visible(self._thank_you_locator)
        elif expect == 'verify':
            self.wait_for_element_visible(self._password_locator)
        else:
            raise Exception('Unknown expect value: %s' % expect)

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

    def click_finish(self):
        """Clicks the 'finish' button."""
        self.selenium.click(self._finish_locator)
        self.wait_for_element_visible(self._thank_you_locator)

    @property
    def thank_you(self):
        """Returns the 'thank you' message."""
        return self.selenium.get_text(self._thank_you_locator)
