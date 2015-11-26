# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from bidpom import BIDPOM
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestAddEmail(BaseTest):

    def test_add_email(self, base_url, selenium, timeout, verified_user, new_email):
        bidpom = BIDPOM(selenium, timeout)
        bidpom.sign_in(verified_user['email'], verified_user['password'])
        WebDriverWait(selenium, timeout).until(lambda s: s.find_element(
            *self._persona_logged_in_indicator_locator).is_displayed())
        self.log_out(selenium, timeout)
        selenium.find_element(*self._persona_login_button_locator).click()

        from bidpom.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.click_add_another_email_address()
        signin.new_email = new_email
        assert signin.new_email == new_email, 'new email getter failed'
        signin.click_add_new_email()
        signin.close_window()
        signin.switch_to_main_window()
        mail = restmail.get_mail(new_email)

        # Check that the email appears to be valid
        self.email_appears_valid(mail[0]['text'])

        selenium.get(re.search(BIDPOM.CONFIRM_URL_REGEX, mail[0]['text']).group(0))
        from bidpom.pages.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(selenium, timeout)
        assert new_email in complete_registration.user_loggedin

        selenium.get(base_url)
        self.log_out(selenium, timeout)

        selenium.find_element(*self._persona_login_button_locator).click()
        signin = SignIn(selenium, timeout)
        assert new_email in signin.emails
        assert new_email == signin.selected_email
