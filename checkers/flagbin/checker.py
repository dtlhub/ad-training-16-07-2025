#!/usr/bin/env python3

import sys

from checklib import *
from flagbin_lib import *


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        super(Checker, self).action(action, *args, **kwargs)

    def check(self):
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        flag_id = self.mch.store_flag(flag)
        self.assert_in(f'{flag_id[:3]}*****', self.mch.list_flags(), Status.CORRUPT)
        self.cquit(Status.OK, f'{flag_id[:3]}*****', flag_id)

    def get(self, flag_id: str, flag: str, vuln: str):
        flag_res = self.mch.retrieve_flag(flag_id)
        self.assert_eq(flag, flag_res, Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
