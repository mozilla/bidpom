#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base


class AccountManager(Base):

    _emails_locator = "id('emailList')/descendant::div[contains(@class, 'email')]"
    _edit_password_button_locator = 'css=#edit_password button.edit'
    _old_password_field_locator = 'id=old_password'
    _new_password_field_locator = 'id=new_password'
    _change_password_done_locator = 'id=changePassword'
    _sign_in_locator = 'css=a.signIn'
    _sign_out_locator = 'css=a.signOut'

    def __init__(self, selenium, timeout):
        Base.__init__(self, selenium, timeout)
        self.wait_for_element_visible('xpath=%s' % self._emails_locator)

    @property
    def emails(self):
        return [self.selenium.get_text('xpath=%s[%s]' % (self._emails_locator, i)) for i in range(1, self.selenium.get_xpath_count(self._emails_locator) + 1)]

    def click_edit_password(self):
        """Click edit password to show the new/old password fields"""
        self.selenium.click(self._edit_password_button_locator)
        self.wait_for_element_visible(self._old_password_field_locator)

    @property
    def old_password(self):
        """Get the value of the old password field."""
        return self.selenium.get_text(self._old_password_field_locator)

    @old_password.setter
    def old_password(self, value):
        """Set the value of the old password field."""
        self.selenium.type(self._old_password_field_locator, value)

    @property
    def new_password(self):
        """Get the value of the new password field."""
        return self.selenium.get_text(self._new_password_field_locator)

    @new_password.setter
    def new_password(self, value):
        """Set the value of the new password field."""
        self.selenium.type(self._new_password_field_locator, value)

    def click_password_done(self):
        """Click password done to save the new password."""
        self.selenium.click(self._change_password_done_locator)
        self.wait_for_element_visible(self._edit_password_button_locator)

    def click_sign_out(self):
        self.selenium.click(self._sign_out_locator)
        self.wait_for_element_visible(self._sign_in_locator)
