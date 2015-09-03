# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

import pytest

from browserid import BrowserID
from base import BaseTest
import restmail


@pytest.mark.nondestructive
class TestResetPassword(BaseTest):

    def test_reset_password(self, selenium, timeout, new_user):
        # sign in as a new user
        from browserid.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.sign_in_new_user(new_user['email'], new_user['password'])
        mail = restmail.get_mail(new_user['email'])
        selenium.get(re.search(BrowserID.VERIFY_URL_REGEX, mail[0]['text']).group(0))
        from browserid.pages.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(selenium, timeout)
        assert new_user['email'] in complete_registration.user_loggedin
        self.log_out(selenium, timeout)

        # forgot password
        selenium.find_element(*self._persona_login_button_locator).click()
        from browserid.pages.sign_in import SignIn
        signin = SignIn(selenium, timeout)
        signin.click_this_is_not_me()
        signin.email = new_user['email']
        signin.click_next()
        signin.click_forgot_password()
        signin.switch_to_main_window()
        mail = restmail.get_mail(new_user['email'], message_count=2)
        assert 'Click to reset your password' in mail[1]['text']

        # reset password
        new_user['password'] = '_{0[password]}'.format(new_user)
        selenium.get(re.search(BrowserID.RESET_URL_REGEX, mail[1]['text']).group(0))
        from browserid.pages.reset_password import ResetPassword
        reset_password = ResetPassword(selenium, timeout)
        reset_password.new_password = new_user['password']
        reset_password.verify_password = new_user['password']
        reset_password.click_finish()
        assert '{0[email]} has been verified!'.format(new_user) in reset_password.thank_you
