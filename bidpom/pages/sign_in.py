# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from base import Base

from selenium.webdriver.common.by import By


class SignIn(Base):

    _form_completing_loading_locator = (By.CSS_SELECTOR, '.form.completing.loading')
    _checking_email_provider_loading_locator = (By.CSS_SELECTOR, '#load .loadingSpinner')
    _this_is_not_me_locator = (By.CSS_SELECTOR, '.isDesktop.thisIsNotMe')
    _signed_in_email_locator = (By.CSS_SELECTOR, 'label[for=email_0]')
    _emails_locator = (By.CSS_SELECTOR, 'label[for^=email_]')
    _email_locator = (By.ID, 'authentication_email')
    _login_password_locator = (By.ID, 'authentication_password')
    _register_password_locator = (By.ID, 'password')
    _verify_password_locator = (By.ID, 'vpassword')
    _desktop_next_locator = (By.CSS_SELECTOR, 'button.isDesktop.isStart')
    _mobile_next_locator = (By.CSS_SELECTOR, 'button.isMobile.isStart')
    _sign_in_locator = (By.CSS_SELECTOR, 'button.isReturning')
    _sign_in_returning_user_locator = (By.ID, 'signInButton')
    _verify_email_locator = (By.ID, 'verify_user')
    _forgot_password_locator = (By.CSS_SELECTOR, '.isDesktop.forgotPassword.left')
    _reset_password_locator = (By.ID, 'password_reset')
    _confirm_message_locator = (By.CSS_SELECTOR, '.contents > p')
    _check_email_at_locator = (By.CSS_SELECTOR, '#wait .contents h2 + p strong')
    _add_another_email_locator = (By.CSS_SELECTOR, '.isDesktop.useNewEmail')
    _new_email_locator = (By.ID, 'newEmail')
    _add_new_email_locator = (By.ID, 'addNewEmail')
    _your_computer_content_locator = (By.ID, 'your_computer_content')
    _this_is_my_computer_locator = (By.ID, 'this_is_my_computer')
    _this_is_not_my_computer_locator = (By.ID, 'this_is_not_my_computer')

    def __init__(self, selenium, timeout=10):
        super(SignIn, self).__init__(selenium, timeout)

        if not self.selenium.title == self._page_title:
            for handle in self.selenium.window_handles:
                self.selenium.switch_to_window(handle)
                self.wait.until(lambda s: s.title)
                if self.selenium.title == self._page_title:
                    self._sign_in_window_handle = handle
                    break
            else:
                raise Exception('Popup has not loaded')

        # Replace expectations with two conditions
        self.wait.until(self._is_page_ready)

    def _is_page_ready(self, s):
        if self.is_element_displayed(*self._email_locator):
            return True
        else:
            body = self.find_element(By.TAG_NAME, 'body')
            sign_in = self.find_element(*self._sign_in_returning_user_locator)
            return sign_in.is_displayed() and 'submit_disabled' not in body.get_attribute('class')

    @property
    def is_initial_sign_in(self):
        """Is this the first sign in for the user?"""
        return self.find_element(*self._email_locator).is_displayed()

    @property
    def signed_in_email(self):
        """Get the value of the email that is currently signed in."""
        return self.find_element(*self._signed_in_email_locator).get_attribute('value')

    def click_this_is_not_me(self):
        """Clicks the 'This is not me' button."""
        self.find_element(*self._this_is_not_me_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._email_locator))

    @property
    def emails(self):
        """Get the emails for the returning user."""
        return [el.text for el in self.find_elements(*self._emails_locator)]

    @property
    def email(self):
        """Get the value of the email field."""
        return self.find_element(*self._email_locator).get_attribute('value')

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = self.find_element(*self._email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def new_email(self):
        """Get the value of the new email field."""
        return self.find_element(*self._new_email_locator).get_attribute('value')

    @new_email.setter
    def new_email(self, value):
        """Set the value of the new email field."""
        email = self.find_element(*self._new_email_locator)
        email.clear()
        email.send_keys(value)

    @property
    def selected_email(self):
        """Return the value of the selected email of returning user's multiple emails"""
        for email in self.find_elements(*self._emails_locator):
            if email.find_element(By.TAG_NAME, 'input').is_selected():
                return email.text

    def select_email(self, value):
        """Select email from the returning user's multiple emails."""
        for email in self.find_elements(*self._emails_locator):
            if email.text == value:
                email.click()
                break
        else:
            raise Exception('Email not found: %s' % value)

    @property
    def register_password(self):
        """Get the value of the register password field."""
        return self.find_element(*self._register_password_locator).get_attribute('value')

    @register_password.setter
    def register_password(self, value):
        """Set the value of the register password field."""
        password = self.find_element(*self._register_password_locator)
        password.clear()
        password.send_keys(value)

    @property
    def login_password(self):
        """Get the value of the login password field."""
        return self.find_element(*self._login_password_locator).get_attribute('value')

    @login_password.setter
    def login_password(self, value):
        """Set the value of the login password field."""
        password = self.find_element(*self._login_password_locator)
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

    @property
    def check_email_at_address(self):
        """Get the value of the email address for confirmation."""
        return self.find_element(*self._check_email_at_locator).text

    def click_next(self, expect='password'):
        """Clicks the 'next' button."""

        if self.is_element_displayed(*self._desktop_next_locator):
            self.find_element(*self._desktop_next_locator).click()
        else:
            self.find_element(*self._mobile_next_locator).click()

        # FIXME: Unfortunately there's no good way to wait for the loading
        # spinner to settle. We can't wait for it to be hidden as it is
        # initially hidden, so we'd continue too soon. We can't reliably wait
        # for it to be visible (and then hidden) because it's often displayed
        # for such a short amount of time that we might miss it due to latency.
        # This has only become an issue in Firefox since Selenium 2.48, which
        # brought the behaviour closer to a real user, and we're effectively
        # clicking the loading message instead of the submit button. The best
        # fix would be for Persona to give us some indication that the loading
        # screen has been displayed but is no longer displayed. For now, I'm
        # going to add a sleep of 5 seconds, which should be plenty of time for
        # the loading screen to appear, if not also disappear. For this, I can
        # only apologise!
        #
        # This is the change in Selenium that caused this:
        # https://github.com/SeleniumHQ/selenium/commit/0eec81da52ba4dfb16de590e6e82ebafa452416f
        #
        # The change has caused others to see similar issues:
        # https://github.com/SeleniumHQ/selenium/issues/1202
        #
        # I have raised the following issue against Persona:
        # https://github.com/mozilla/persona/issues/4227
        #
        # Note that this is not a bug in Selenium, it is an enhancement that
        # has highlighted an issue with our Persona automation.
        time.sleep(5)

        loading = self.find_element(*self._checking_email_provider_loading_locator)
        self.wait.until(lambda s: not loading.is_displayed())

        if expect == 'password':
            body = self.find_element(By.TAG_NAME, 'body')
            self.wait.until(lambda s: self.is_element_displayed(*self._login_password_locator))
            self.wait.until(lambda s: 'returning' in body.get_attribute('class'))
        elif expect == 'verify':
            self.wait.until(lambda s: self.is_element_displayed(*self._verify_email_locator))
        else:
            raise Exception('Unknown expect value: %s' % expect)

    def click_sign_in(self):
        """Clicks the 'sign in' button."""
        self.find_element(*self._sign_in_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._form_completing_loading_locator))
        self.wait.until(lambda s: self._sign_in_window_handle not in self.selenium.window_handles)
        self.switch_to_main_window()

    def click_sign_in_returning_user(self, expect=None):
        """Clicks the 'sign in' button."""
        self.find_element(*self._sign_in_returning_user_locator).click()

        time.sleep(5)
        if len(self.selenium.window_handles) == 1:
            self.switch_to_main_window()
        else:
            self.wait.until(lambda s: self.is_element_displayed(
                *self._your_computer_content_locator))

    def click_verify_email(self):
        """Clicks 'verify email' button."""
        self.find_element(*self._verify_email_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._check_email_at_locator))

    def click_forgot_password(self):
        """Clicks 'forgot password' link (visible after entering a valid email)"""
        self.find_element(*self._forgot_password_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._confirm_message_locator))

    def click_reset_password(self):
        """Clicks 'reset password' after forgot password and new passwords entered"""
        self.find_element(*self._reset_password_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._check_email_at_locator))

    def click_add_another_email_address(self):
        """Clicks 'add another email' button."""
        self.find_element(*self._add_another_email_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._add_new_email_locator))

    def click_add_new_email(self):
        """Clicks 'Add' button to insert new email address."""
        self.find_element(*self._add_new_email_locator).click()
        self.wait.until(lambda s: self.is_element_displayed(*self._check_email_at_locator))

    def click_i_trust_this_computer(self):
        """Clicks 'I trust this computer' and signs in """
        self.find_element(*self._this_is_my_computer_locator).click()
        self.switch_to_main_window()

    def click_this_is_not_my_computer(self):
        """Clicks 'I trust this computer' and signs in for a public computer"""
        self.find_element(*self._this_is_not_my_computer_locator).click()
        self.switch_to_main_window()

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        self.click_next(expect='password')
        self.login_password = password
        self.click_sign_in()

    def sign_in_new_user(self, email, password):
        """Requests verification email using the specified email address."""
        self.email = email
        self.click_next(expect='verify')
        self.register_password = password
        self.verify_password = password
        self.click_verify_email()
        self.close_window()
        self.switch_to_main_window()

    def sign_in_returning_user(self):
        """Signs in with the stored user."""
        self.click_sign_in_returning_user()
