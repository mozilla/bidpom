# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class BaseTest(object):

    _persona_login_button_locator = (By.CSS_SELECTOR, 'button.btn-persona')
    _persona_logged_in_indicator_locator = (By.ID, 'loggedin')
    _persona_log_out_link_locator = (By.CSS_SELECTOR, '#loggedin a')

    def log_out(self, selenium, timeout=10):
        WebDriverWait(selenium, timeout).until(
            lambda s: s.find_element(*self._persona_logged_in_indicator_locator).is_displayed())
        selenium.find_element(*self._persona_log_out_link_locator).click()
        WebDriverWait(selenium, timeout).until(
            lambda s: s.find_element(*self._persona_login_button_locator).is_displayed())

    def email_appears_valid(self, email_text):
        assert 'Click' in email_text and 'link' in email_text, \
            'The strings "Click" and "link" were not found in %s' % email_text
