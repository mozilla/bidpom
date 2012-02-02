#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base


class SignIn(Base):

    _email_locator = 'id=email'
    _password_locator = 'id=password'
    _next_locator = 'css=button.start'
    _select_email_locator = 'css=button.returning'
    _sign_in_locator = 'id=signInButton'

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.wait_for_element_visible(self._email_locator)

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.get_text(self._email_locator)

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        self.selenium.type(self._email_locator, value)

    @property
    def password(self):
        """Get the value of the password field."""
        return self.selenium.get_text(self._password_locator)

    @password.setter
    def password(self, value):
        """Set the value of the password field."""
        self.selenium.type(self._password_locator, value)

    def click_next(self):
        """Clicks the 'next' button."""
        self.selenium.click(self._next_locator)
        self.wait_for_element_visible(self._select_email_locator)

    def click_select_email(self):
        """Clicks the 'select email' button."""
        self.selenium.click(self._select_email_locator)
        self.wait_for_element_visible(self._sign_in_locator)

    def click_sign_in(self):
        """Clicks the 'Sign In' button."""
        self.selenium.click(self._sign_in_locator)
        self.selenium.deselect_pop_up()

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next()
        self.password = password
        self.click_select_email()
        self.click_sign_in()
