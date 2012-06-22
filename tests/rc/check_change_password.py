#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from ... import BrowserID
from base import BaseTest


@pytest.mark.nondestructive
class TestSignIn(BaseTest):

    @pytest.mark.travis
    def test_change_password(self, mozwebqa):
        (email, password) = self.create_verified_user(mozwebqa.selenium,
                                                      mozwebqa.timeout)

        mozwebqa.selenium.open('https://login.dev.anosrep.org')
        from ...pages.rc.account_manager import AccountManager
        account_manager = AccountManager(mozwebqa.selenium, mozwebqa.timeout)

        assert email in account_manager.emails

        account_manager.click_edit_password()
        account_manager.old_password = password
        new_password = password + '_new'
        account_manager.new_password = new_password
        account_manager.click_password_done()
        account_manager.click_sign_out()

        mozwebqa.selenium.open('%s/' % mozwebqa.base_url)

        login_locator = 'css=#loggedout button'
        mozwebqa.wait_for_element_visible(mozwebqa, login_locator)
        mozwebqa.selenium.click(login_locator)

        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in(email, new_password)

        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)
