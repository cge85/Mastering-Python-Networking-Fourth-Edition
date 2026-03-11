#!/usr/bin/env python3

import requests
import json
import pprint
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url='https://192.168.0.20/ins'
switchuser='admin'
switchpassword='cisco'

myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
]
response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser,switchpassword), verify=False).json()

print(response['result']['body']['nxos_ver_str'])

