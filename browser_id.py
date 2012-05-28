#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import selenium


class BrowserID(object):

    VERIFY_URL_REGEX = 'https?:\/\/(\S+)\/verify_email_address\?token=(\S+)'

    def __init__(self, sel, timeout=60):
        self.selenium = sel
        setattr(self.selenium, 'rc', isinstance(self.selenium,
                                                selenium.selenium))
        self.timeout = timeout

    def sign_in(self, email=None, password=None):
        """Signs in using the specified email address and password."""
        if self.selenium.rc:
            from pages.rc.sign_in import SignIn
        else:
            from pages.webdriver.sign_in import SignIn
        if email and password:
            sign_in = SignIn(self.selenium, timeout=self.timeout, expect='new')
            sign_in.sign_in(email, password)
        elif email:
            sign_in = SignIn(self.selenium, timeout=self.timeout, expect='new')
            sign_in.sign_in_new_user(email)
        else:
            sign_in = SignIn(self.selenium,
                             timeout=self.timeout,
                             expect='returning')
            sign_in.sign_in_returning_user()
