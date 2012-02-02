#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from .. import BrowserID

from selenium import webdriver
from selenium import selenium

class TestSignIn:

    _email = ''
    _password = ''

    def test_sign_in_to_my_favorite_beer_using_webdriver(self):
        sel = webdriver.Firefox()
        sel.implicitly_wait(10)
        sel.get('http://myfavoritebeer.org/')
        sel.find_element_by_css_selector('#loginInfo .login').click()
        sel.implicitly_wait(0)
    
        # BrowserID
        browser_id = BrowserID(sel)
        browser_id.sign_in(self._email, self._password)

        sel.implicitly_wait(10)
        assert sel.find_element_by_id('logout').is_displayed
        sel.quit()
    
    def test_sign_in_to_my_favorite_beer_using_rc(self):
        sel = selenium('localhost', '4444', '*firefox', 'http://myfavoritebeer.org')
        sel.start()
        sel.open('/')
        sel.click('css=#loginInfo .login')
    
        # BrowserID
        browser_id = BrowserID(sel)
        browser_id.sign_in(self._email, self._password)
    
        logout_locator = 'id=logout'
        count = 0
        while count < 60 and not (sel.is_element_present(logout_locator) and sel.is_visible(logout_locator)):
            time.sleep(1)
            count += 1
        assert sel.is_visible('id=logout')
        sel.stop()
