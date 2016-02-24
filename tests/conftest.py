# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import urllib2
import uuid

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope='session')
def session_capabilities(session_capabilities):
    session_capabilities.setdefault('tags', []).append('bidpom')
    return session_capabilities


@pytest.fixture
def new_email():
    return 'bidpom_{0}@restmail.net'.format(uuid.uuid1())


@pytest.fixture
def new_user(new_email):
    return {'email': new_email, 'password': 'password'}


@pytest.fixture
def selenium(base_url, selenium, timeout):
    selenium.get(base_url)
    sign_in = selenium.find_element(By.CSS_SELECTOR, 'button.btn-persona')
    WebDriverWait(selenium, timeout).until(lambda s: sign_in.is_displayed())
    sign_in.click()
    return selenium


@pytest.fixture
def timeout():
    return 10


@pytest.fixture
def verified_user():
    response = urllib2.urlopen('http://personatestuser.org/email/stage').read()
    user = json.loads(response)
    return {'email': user['email'],
            'password': user['pass']}
