#!/usr/bin/env python3

import sys
import requests

from checklib import *
from example_lib import *
from random import sample, randint

def rnd_type():
    return sample(['Melee', 'Magic'], 1)[0]

class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
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
        char_name,char_type, username, password = rnd_username(), rnd_type(), rnd_username(), rnd_password()
        secret_answer = rnd_string(10)


        self.mch.register(session, username, password, secret_answer)
        self.mch.login(session, username, password,secret_answer, Status.MUMBLE)
        #value = self.mch.recover_password(session, username, password,secret_answer)
        #self.assert_eq(value, True, "Tech support not working")
        self.mch.create_char(session, char_name, char_type, randint(1,6))
        self.mch.select_char(session)

        for _ in range(10):
            self.mch.play(session)

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        username, password = rnd_username(), rnd_password()
        char_name, char_type = rnd_username(), rnd_type()
        self.mch.register(session, username, password, flag)
        self.mch.login(session, username, password, flag, Status.MUMBLE)
        self.mch.create_char(session, char_name, char_type, randint(1,6))
        self.mch.select_char(session)

        for _ in range(20):
            self.mch.play(session, 'pvp')
        self.cquit(Status.OK, f'{username}:{password}', f'{username}:{password}')

    def get(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        username, password = flag_id.split(':')

        self.mch.login(session, username, password, flag,Status.CORRUPT)
        #value = self.mch.recover_password(session, username, password,flag)
        #self.assert_eq(value, True, "Tech support not working", Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
