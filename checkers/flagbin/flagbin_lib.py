from checklib import *
from pwnlib.tubes.remote import *

PORT = 52420


class CheckMachine:
    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def store_flag(self, flag: str) -> str:
        r = remote(self.c.host, self.port)

        r.sendlineafter(b'--> ', b'1')
        r.sendlineafter(b': ', flag.encode())
        r.recvuntil(b': ')

        flag_id = r.recvuntil(b'\n').decode()

        r.close()
        return flag_id

    def retrieve_flag(self, flag_id: str) -> str:
        r = remote(self.c.host, self.port)

        r.sendlineafter(b'--> ', b'2')
        r.sendlineafter(b': ', flag_id.encode())
        r.sendlineafter(b': ', b'0')

        flag = r.recvline().decode().strip()

        r.close()
        return flag


    def list_flags(self) -> str:
        r = remote(self.c.host, self.port)

        r.sendlineafter(b'--> ', b'3')
        flags = r.recvuntil(b'[1]').decode()

        r.close()
        return flags
