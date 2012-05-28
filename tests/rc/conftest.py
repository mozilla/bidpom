#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time


def pytest_runtest_setup(item):
    item.config.option.api = 'rc'


def pytest_funcarg__mozwebqa(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')
    mozwebqa.wait_for_element_visible = wait_for_element_visible
    mozwebqa.selenium.open('%s/' % mozwebqa.base_url)
    login_locator = 'css=#loggedout button'
    wait_for_element_visible(mozwebqa, login_locator)
    mozwebqa.selenium.click(login_locator)
    return mozwebqa


def wait_for_element_visible(mozwebqa, locator):
    end_time = time.time() + mozwebqa.timeout
    while(True):
        if mozwebqa.selenium.is_visible(locator):
            return True
        time.sleep(0.5)
        if(time.time() > end_time):
            break
    raise Exception('Timeout waiting for element to be visible: %s' % locator)
