# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class BrowserID(object):

    VERIFY_URL_REGEX = 'https?:\/\/(\S+)\/verify_email_address\?token=(.{48})'
    CONFIRM_URL_REGEX = 'https?:\/\/(\S+)\/confirm\?token=(.{48})'
    RESET_URL_REGEX = 'https?:\/\/(\S+)\/reset_password\?token=(.{48})'
    INCLUDE_URL_REGEX = '(https?:\/\/(\S+))\/include\.js'

    def __init__(self, selenium, timeout=60):
        self.selenium = selenium
        self.timeout = timeout

    def sign_in(self, email=None, password=None):
        """Signs in a user, either with the specified email address and password, or a returning user."""
        from pages.sign_in import SignIn
        sign_in = SignIn(self.selenium, timeout=self.timeout)
        if sign_in.is_initial_sign_in:
            sign_in.sign_in(email, password)
        else:
            sign_in.sign_in_returning_user()
            if len(self.selenium.window_handles) == 2:
                sign_in.click_this_is_not_my_computer()
                sign_in.switch_to_main_window()
