#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def pytest_runtest_setup(item):
    item.config.option.api = 'webdriver'


def pytest_funcarg__mozwebqa(request):
    mozwebqa = request.getfuncargvalue('mozwebqa')
    mozwebqa.selenium.implicitly_wait(10)
    mozwebqa.selenium.get('%s/' % mozwebqa.base_url)
    mozwebqa.selenium.find_element_by_id('loggedout'). \
        find_element_by_tag_name('button').click()
    mozwebqa.selenium.implicitly_wait(0)
    return mozwebqa
