#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException


class Base(object):

    _page_title = 'Mozilla Persona: A Better Way to Sign In'

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout
        self._main_window_handle = self.selenium.current_window_handle

    def switch_to_main_window(self):
        self.selenium.switch_to_window(self._main_window_handle)

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(0)
