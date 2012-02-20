#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time


class Base(object):

    _page_title = 'BrowserID'

    def __init__(self, selenium, timeout=60000):
        self.selenium = selenium
        self.timeout = timeout
        if selenium.get_title != self._page_title:
            self.wait_for_popup()
            selenium.select_pop_up(self._page_title)

    def wait_for_popup(self):
        count = 0
        while not self._page_title in self.selenium.get_all_window_titles():
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception('Popup has not loaded')

    def wait_for_element_present(self, element):
        count = 0
        while not self.selenium.is_element_present(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception(element + ' has not loaded')

    def wait_for_element_visible(self, element):
        self.wait_for_element_present(element)
        count = 0
        while not self.selenium.is_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception(element + ' is not visible')
