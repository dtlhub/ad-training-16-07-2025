#!/usr/bin/env python3

import sys
import requests

from checklib import *
from nevalashka_lib import *


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 15
    uses_attack_data: bool = False

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        pub_text = rnd_string(20)

        self.mch.register(session, username, password)
        self.mch.login(session, username, password, Status.MUMBLE)
        self.mch.put_publication(session, pub_text)
        value = self.mch.get_publication(session, pub_text, Status.MUMBLE)

        self.assert_eq(value, pub_text, "Publication text is invalid")

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()

        self.mch.register(session, username, password)
        self.mch.login(session, username, password, Status.MUMBLE)
        self.mch.put_publication(session, flag)

        filename = self.mch.get_filename(session, flag)

        self.cquit(Status.OK, f'{filename[4:]}', f'{username}:{password}:{filename}')

    def get(self, flag_id: str, flag: str, vuln: str):
        s = get_initialized_session()
        username, password, filename = flag_id.split(':')

        self.mch.login(s, username, password, Status.CORRUPT)
        value = self.mch.get_publication(s, filename, Status.CORRUPT)

        self.assert_eq(value, flag, "Publication is invalid", Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
