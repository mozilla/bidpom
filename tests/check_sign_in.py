# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait

from browserid import BrowserID
from mocks.user import MockUser
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestSignIn(BaseTest):

    def test_sign_in_helper(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in(self, mozwebqa):
        from browserid.pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.email = mozwebqa.email
        assert signin.email == mozwebqa.email, "email getter failed"
        signin.click_next(expect='password')
        signin.login_password = mozwebqa.password
        assert signin.login_password == mozwebqa.password, "password getter failed"
        signin.click_sign_in()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    @pytest.mark.travis
    def test_sign_in_new_user_helper(self, mozwebqa):
        user = MockUser()
        from browserid.pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        print 'signing in as %s' % user.primary_email
        signin.sign_in_new_user(user.primary_email, 'password')
        mail = restmail.get_mail(user.primary_email, timeout=mozwebqa.timeout)

        # Check that the email appears to be valid
        self.email_appears_valid(mail[0]['text'])

    @pytest.mark.travis
    def test_sign_in_new_user(self, mozwebqa):
        user = MockUser()
        from browserid.pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        print 'signing in as %s' % user.primary_email
        signin.email = user.primary_email
        signin.click_next(expect='verify')
        signin.register_password = user.password
        signin.verify_password = user.password
        assert signin.verify_password == user.password, 'verify password getter failed'
        signin.click_verify_email()
        assert signin.check_email_at_address == user.primary_email

        signin.close_window()
        signin.switch_to_main_window()
        mail = restmail.get_mail(user.primary_email, timeout=mozwebqa.timeout)

        # Check that the email appears to be valid
        self.email_appears_valid(mail[0]['text'])

    @pytest.mark.travis
    def test_sign_in_returning_user(self, mozwebqa):
        self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_is_this_your_computer_immediately(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

        self.log_out(mozwebqa.selenium, mozwebqa.timeout)

        mozwebqa.selenium.find_element(*self._persona_login_button_locator).click()

        from browserid.pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.click_sign_in_returning_user()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_helper_with_returning_user(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

        self.log_out(mozwebqa.selenium, mozwebqa.timeout)

        self._wait_to_delay_next_login(mozwebqa.selenium)

        mozwebqa.selenium.find_element(*self._persona_login_button_locator).click()

        browser_id.sign_in()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    def test_sign_in_helper_with_returning_user_immediately(self, mozwebqa):
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

        self.log_out(mozwebqa.selenium, mozwebqa.timeout)

        mozwebqa.selenium.find_element(*self._persona_login_button_locator).click()

        browser_id.sign_in()

        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())

    def _wait_to_delay_next_login(self, selenium):
        # We cannot just sleep for 60 seconds as the browser will timeout after 30 seconds
        start_time = time.time()
        while time.time() < (start_time + 60):
            time.sleep(15)
            selenium.find_element(*self._persona_login_button_locator)
