#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time

import requests


def get_mail(username, timeout=60):
    end_time = time.time() + timeout
    while(True):
        response = requests.get(
            'https://restmail.net/mail/%s' % username,
            verify=False)
        restmail = json.loads(response.content)
        if len(restmail) > 0:
            return restmail
        time.sleep(0.5)
        if(time.time() > end_time):
            break
    raise Exception('Timeout getting restmail for %s' % username)
