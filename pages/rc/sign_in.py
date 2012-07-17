#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base


class SignIn(Base):

    _signed_in_email_locator = 'css=label[for=email_0]'
    _email_locator = 'id=email'
    _password_locator = 'id=password'
    _verify_password_locator = 'id=vpassword'
    _next_locator = 'css=button.start'
    _sign_in_locator = 'css=button.returning'
    _sign_in_returning_user_locator = 'id=signInButton'
    _verify_email_locator = 'id=verify_user'
    _check_email_at_locator = 'css=#wait .contents h2 + p strong'

    def __init__(self, selenium, timeout, expect='new'):
        Base.__init__(self, selenium, timeout)

        if self.selenium.get_title != self._page_title:
            self.wait_for_popup(self._page_title)
            self.selenium.select_pop_up(self._page_title)

        if expect == 'new':
            self.wait_for_element_visible(self._email_locator)
        elif expect == 'returning':
            self.wait_for_element_visible(self._sign_in_returning_user_locator)
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def close_window(self):
        self.selenium.close()

    @property
    def signed_in_email(self):
        """Get the value of the email that is currently signed in."""
        return self.selenium.get_text(self._signed_in_email_locator)

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

    @property
    def verify_password(self):
        """Get the value of the verify password field."""
        return self.selenium.get_text(self._verify_password_locator)

    @password.setter
    def verify_password(self, value):
        """Set the value of the verify password field."""
        self.selenium.type(self._verify_password_locator, value)

    @property
    def check_email_at_address(self):
        """Get the value of the email address for confirmation."""
        return self.selenium.get_text(self._check_email_at_locator)

    def click_next(self, expect='password'):
        """Clicks the 'next' button."""
        self.selenium.click(self._next_locator)
        if expect == 'password':
            self.wait_for_element_visible(self._password_locator)
        elif expect == 'verify':
            self.wait_for_element_visible(self._verify_email_locator)
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_sign_in(self):
        """Clicks the 'Sign In' button."""
        self.selenium.click(self._sign_in_locator)
        self.selenium.deselect_pop_up()

    def click_sign_in_returning_user(self):
        """Clicks the 'sign in' button."""
        self.selenium.click(self._sign_in_returning_user_locator)
        self.selenium.deselect_pop_up()

    def click_verify_email(self):
        """Clicks 'verify email' button."""
        self.selenium.click(self._verify_email_locator)
        self.wait_for_element_visible(self._check_email_at_locator)

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next(expect='password')
        self.password = password
        self.click_sign_in()

    def sign_in_new_user(self, email, password):
        """Requests verification email using the specified email address."""
        self.email = email
        self.click_next(expect='verify')
        self.password = password
        self.verify_password = password
        self.click_verify_email()
        self.close_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self):
        """Signs in with the stored user."""
        self.click_sign_in_returning_user()
