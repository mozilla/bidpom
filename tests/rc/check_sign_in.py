#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.mark.nondestructive
class TestSignIn:

    def test_sign_in_helper(self, mozwebqa):
        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium)
        browser_id.sign_in(mozwebqa.email, mozwebqa.password)

        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)

    def test_sign_in(self, mozwebqa):
        from ...pages.rc.sign_in import SignIn
        signin = SignIn(mozwebqa.selenium, mozwebqa.timeout)
        signin.email = mozwebqa.email
        signin.click_next()
        signin.password = mozwebqa.password
        signin.click_sign_in()

        logout_locator = 'css=#loggedin a'
        mozwebqa.wait_for_element_visible(mozwebqa, logout_locator)
        assert mozwebqa.selenium.is_visible(logout_locator)
