#!/usr/bin/env python3

# Читает любой файл либо из /var/www/html/receipts, либо по указанному пути 

import sys
import requests

ip = sys.argv[1]
filename = sys.argv[2]

url = f"http://{ip}:7000/readPub.php?fnPubilcation={filename}&fnSuccess=1"

r = requests.get(url)

print(r.text)
