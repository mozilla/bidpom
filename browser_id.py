#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import selenium


class BrowserID(object):

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        if isinstance(self.selenium, selenium.selenium):
            from pages.rc.sign_in import SignIn
        else:
            from pages.webdriver.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout)
        sign_in.sign_in(email, password)
