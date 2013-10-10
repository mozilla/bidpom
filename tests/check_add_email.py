#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import pytest

from browserid import BrowserID
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestAddEmail(BaseTest):

    @pytest.mark.travis
    def test_add_email(self, mozwebqa):
        user = self.create_verified_user(mozwebqa.selenium, mozwebqa.timeout)
        user.additional_emails.append('%s_1@restmail.net' % user.id)

        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        self.log_out(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.find_element(*self._persona_login_button_locator).click()

        from browserid.pages.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.click_add_another_email_address()
        signin.new_email = user.additional_emails[0]
        assert signin.new_email == user.additional_emails[0], "new email getter failed"
        signin.click_add_new_email()
        signin.close_window()
        signin.switch_to_main_window()

        mail = restmail.get_mail(user.additional_emails[0],
                                 timeout=mozwebqa.timeout)
        assert 'Click this link to confirm access' in mail[0]['text']
        confirm_url = re.search(
            BrowserID.CONFIRM_URL_REGEX, mail[0]['text']).group(0)

        mozwebqa.selenium.get(confirm_url)
        from browserid.pages.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(mozwebqa.selenium,
                                                     mozwebqa.timeout,
                                                     expect='success')
        assert user.additional_emails[0] in complete_registration.user_loggedin

        mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
        self.log_out(mozwebqa.selenium, mozwebqa.timeout)
        mozwebqa.selenium.find_element(*self._persona_login_button_locator).click()

        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        assert user.additional_emails[0] in signin.emails
        assert signin.selected_email == user.additional_emails[0]
