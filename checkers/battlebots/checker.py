#!/usr/bin/env python3

import sys

from checklib import *
from battlebots_lib import *


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 10
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        super(Checker, self).action(action, *args, **kwargs)

    def check(self):
        self.mch.connect()

        h, s, a = self.mch.view(1)
        self.assert_eq(h, 0, Status.MUMBLE)
        self.assert_eq(s, 0, Status.MUMBLE)
        self.assert_eq(a, 0, Status.MUMBLE)

        self.mch.edit(3, 3, 4, 5)
        h, s, a = self.mch.view(3)
        self.assert_eq(h, 3, Status.MUMBLE)
        self.assert_eq(s, 4, Status.MUMBLE)
        self.assert_eq(a, 5, Status.MUMBLE)

        cooked = self.mch.battle()
        self.assert_eq(cooked, [0, 1, 2, 4], Status.MUMBLE)

        self.mch.disconnect()
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        self.mch.connect()

        fid = self.mch.leave_feedback(flag, None)

        self.mch.disconnect()
        self.cquit(Status.OK, f'{str(fid)[:2]}*****', fid)

    def get(self, flag_id: str, flag: str, vuln: str):
        self.mch.connect()

        flag_res = self.mch.leave_feedback('', flag_id)
        self.assert_in(flag, flag_res, Status.CORRUPT)

        self.mch.disconnect()
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
    except Exception as e:
        cquit(Status.MUMBLE, str(e), str(e))
