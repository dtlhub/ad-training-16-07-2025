from checklib import *
from pwnlib.tubes.remote import *

PORT = 55555


class CheckMachine:
    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT
        self.r = None

    def connect(self):
        self.r = remote(self.c.host, self.port)

    def disconnect(self):
        self.r.sendline(b'5')
        self.r.close()
        self.r = None

    def view(self, bid):
        self.r.sendlineafter(b'  --> ', b'1')
        self.r.sendlineafter(b'Battlebot ID > ', str(bid).encode())

        self.r.recvuntil(b'Battlebot ')
        self.r.recvuntil(b'HP: ')
        hp = int(self.r.recvuntil(b'\n'))
        self.r.recvuntil(b'SHD: ')
        shd = int(self.r.recvuntil(b'\n'))
        self.r.recvuntil(b'ATK: ')
        atk = int(self.r.recvuntil(b'\n'))
    
        return hp, shd, atk
    
    def edit(self, bid, hp, shd, atk):
        self.r.sendlineafter(b'  --> ', b'2')
        self.r.sendlineafter(b'Battlebot ID > ', str(bid).encode())
    
        self.r.sendlineafter(b'HP > ', str(hp).encode())
        self.r.sendlineafter(b'SHD > ', str(shd).encode())
        self.r.sendlineafter(b'ATK > ', str(atk).encode())

    def battle(self):
        cooked = []

        self.r.sendlineafter(b'  --> ', b'3')
        self.r.recvuntil(b'Let the battle begin!\n')

        for i in range(4):
            self.r.recvuntil(b'Battlebot ')
            cooked.append(int(self.r.recvuntil(b' ')))
            self.r.recvuntil(b'is cooked!\n')

        return cooked
    
    def leave_feedback(self, feedback, chat_id):
        self.r.sendlineafter(b'  --> ', b'4')
        if chat_id is None:
            self.r.sendlineafter(b'Do you have a chat id? [y/n] > ', b'n')
            self.r.sendlineafter(b'Enter your feedback > ', feedback.encode())
            self.r.recvuntil(b'Your feedback was saved! You can chat with our developers using this chad id: ')
            fid = self.r.recvuntil(b'\n').decode()
            return int(fid)
        else:
            self.r.sendlineafter(b'Do you have a chat id? [y/n] > ', b'y')
            self.r.sendlineafter(b'Chat id > ', str(chat_id).encode())
            self.r.recvuntil(b'Chat history:')
            hist = self.r.recvuntil(b'Enter your message > ')
            self.r.sendline(feedback.encode())
            return hist.decode()
