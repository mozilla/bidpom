# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException


class Base(object):

    _page_title = 'Mozilla Persona: A Better Way to Sign In'

    def __init__(self, selenium, timeout=60, default_implicit_wait=10):
        self.selenium = selenium
        self.timeout = timeout
        self.default_implicit_wait = default_implicit_wait
        self._main_window_handle = self.selenium.current_window_handle

    def switch_to_main_window(self):
        self.selenium.switch_to_window(self._main_window_handle)

    def is_element_present(self, *locator):
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def close_window(self):
        self.selenium.close()
