from checklib import *
from pwnlib.tubes.remote import *

PORT = 52420


class CheckMachine:
    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT
        self.r = None

    def connect(self):
        self.r = remote(self.c.host, self.port)

    def disconnect(self):
        self.r.close()
        self.r = None

    def store_flag(self, flag: str) -> str:
        self.r.sendlineafter(b'--> ', b'1')
        self.r.sendlineafter(b'Flag: ', flag.encode())
        self.r.recvuntil(b'Flag id: ')

        flag_id = self.r.recvuntil(b'\n').decode()

        return flag_id

    def retrieve_flag(self, flag_id: str) -> str:
        self.r.sendlineafter(b'--> ', b'2')
        self.r.sendlineafter(b'Flag id: ', flag_id.encode())
        self.r.sendlineafter(b'Offset: ', b'0')

        flag = self.r.recvline().decode().strip()

        return flag

    def list_flags(self) -> str:
        self.r.sendlineafter(b'--> ', b'3')
        flags = self.r.recvuntil(b'[1]').decode()

        return flags
