#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import uuid

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from .. import restmail


@pytest.mark.nondestructive
class TestVerifyEmailAddress:

    def test_verify_email_address_helper(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()

        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in('%s@restmail.net' % restmail_username)
        mail = restmail.get_mail(restmail_username)
        verify_url = re.search(BrowserID.VERIFY_URL_REGEX,
                               mail[0]['text']).group(0)
        mozwebqa.selenium.get(verify_url)

        from ...pages.webdriver.verify_email_address import VerifyEmailAddress
        verify_email_address = VerifyEmailAddress(mozwebqa.selenium,
                                                  mozwebqa.timeout)
        verify_email_address.verify_email_address('password')

    def test_verify_email_address(self, mozwebqa):
        restmail_username = 'bidpom_%s' % uuid.uuid1()

        from ... import BrowserID
        browser_id = BrowserID(mozwebqa.selenium, mozwebqa.timeout)
        browser_id.sign_in('%s@restmail.net' % restmail_username)
        mail = restmail.get_mail(restmail_username)
        verify_url = re.search(BrowserID.VERIFY_URL_REGEX,
                               mail[0]['text']).group(0)
        mozwebqa.selenium.get(verify_url)

        from ...pages.webdriver.verify_email_address import VerifyEmailAddress
        verify_email_address = VerifyEmailAddress(mozwebqa.selenium,
                                                  mozwebqa.timeout)
        verify_email_address.password = 'password'
        verify_email_address.verify_password = 'password'
        verify_email_address.click_finish()
