# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from bidpom import BIDPOM
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestSignIn(BaseTest):

    def test_sign_in_helper(self, selenium, timeout, verified_user):
        bidpom = BIDPOM(selenium, timeout)
        bidpom.sign_in(verified_user['email'], verified_user['password'])
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in(self, selenium, timeout, verified_user):
        from bidpom.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.email = verified_user['email']
        assert signin.email == verified_user['email']
        signin.click_next(expect='password')
        signin.login_password = verified_user['password']
        assert signin.login_password == verified_user['password']
        signin.click_sign_in()
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_new_user_helper(self, new_user, selenium, timeout):
        from bidpom.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.sign_in_new_user(new_user['email'], new_user['password'])
        mail = restmail.get_mail(new_user['email'])

        # Check that the email appears to be valid
        self.email_appears_valid(mail[0]['text'])

    def test_sign_in_new_user(self, new_user, selenium, timeout):
        from bidpom.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.email = new_user['email']
        signin.click_next(expect='verify')
        signin.register_password = new_user['password']
        signin.verify_password = new_user['password']
        assert signin.verify_password == new_user['password'], 'verify password getter failed'
        signin.click_verify_email()
        assert signin.check_email_at_address == new_user['email']

        signin.close_window()
        signin.switch_to_main_window()
        mail = restmail.get_mail(new_user['email'])

        # Check that the email appears to be valid
        self.email_appears_valid(mail[0]['text'])

    def test_sign_in_is_this_your_computer_immediately(self, selenium, timeout, verified_user):
        bidpom = BIDPOM(selenium, timeout)
        bidpom.sign_in(verified_user['email'], verified_user['password'])
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())
        self.log_out(selenium, timeout)

        selenium.find_element(*self._persona_login_button_locator).click()

        from bidpom.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.click_sign_in_returning_user()
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_helper_with_returning_user(self, selenium, timeout, verified_user):
        bidpom = BIDPOM(selenium, timeout)
        bidpom.sign_in(verified_user['email'], verified_user['password'])
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())
        self.log_out(selenium, timeout)

        self._wait_to_delay_next_login(selenium)
        selenium.find_element(*self._persona_login_button_locator).click()
        bidpom.sign_in()
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_helper_with_returning_user_immediately(self, selenium, timeout, verified_user):
        bidpom = BIDPOM(selenium, timeout)
        bidpom.sign_in(verified_user['email'], verified_user['password'])
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())
        self.log_out(selenium, timeout)
        selenium.find_element(*self._persona_login_button_locator).click()
        bidpom.sign_in()
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())

    def _wait_to_delay_next_login(self, selenium):
        # We cannot just sleep for 60 seconds as the browser will timeout after 30 seconds
        start_time = time.time()
        while time.time() < (start_time + 60):
            time.sleep(15)
            selenium.find_element(*self._persona_login_button_locator)
