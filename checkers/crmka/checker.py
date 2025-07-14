#!/usr/bin/env python3

import sys
import requests

from checklib import *
from crmka_lib import *

class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
    uses_attack_data: bool = True

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
        account_name = self.mch.get_account_name(session)

        set_jwt(session, account_name)

        artist = Artist(rnd_username(10), rnd_string(10))
        _id = self.mch.put_entity(session, artist)
        value = self.mch.get_entity(session, _id, artist.model_name, Status.MUMBLE)
        self.assert_eq(value['name'], artist.name, "Entity value is invalid")
        self.assert_eq(value['contact'], artist.contact, "Entity value is invalid")

        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        account_name = self.mch.get_account_name(session)
        
        set_jwt(session, account_name)
        
        artist = Artist(rnd_username(10), flag)
        _id = self.mch.put_entity(session, artist)

        self.cquit(Status.OK, artist.name, f'{artist.name}:{artist.model_name}:{_id}')

    def get(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        account_name = self.mch.get_account_name(session)
        
        set_jwt(session, account_name)

        name, model_name, _id = flag_id.split(':')

        value = self.mch.get_entity(session, _id, model_name, Status.CORRUPT)
        self.assert_eq(value['contact'], flag, "Artist contact value is invalid", Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
