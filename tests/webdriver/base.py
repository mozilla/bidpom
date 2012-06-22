#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import uuid

import requests

from ... import BrowserID
from .. import restmail


class BaseTest(object):

    def browserid_url(self, base_url):
        response = requests.get('%s/' % base_url, verify=False)
        match = re.search(BrowserID.INCLUDE_URL_REGEX, response.content)
        if match:
            return match.group(1)
        else:
            raise Exception('Unable to determine BrowserID URL from %s.' % base_url)

    def create_verified_user(self, selenium, timeout):
        restmail_username = 'bidpom_%s' % uuid.uuid1()
        email = '%s@restmail.net' % restmail_username
        password = 'password'

        from ...pages.webdriver.sign_in import SignIn
        signin = SignIn(selenium, timeout, expect='new')
        signin.sign_in_new_user(email, password)
        mail = restmail.get_mail(restmail_username)
        verify_url = re.search(BrowserID.VERIFY_URL_REGEX,
                               mail[0]['text']).group(0)

        selenium.get(verify_url)
        from ...pages.webdriver.complete_registration import CompleteRegistration
        complete_registration = CompleteRegistration(selenium,
                                                     timeout,
                                                     expect='success')
        assert 'Thank you' in complete_registration.thank_you
        return (email, password)
