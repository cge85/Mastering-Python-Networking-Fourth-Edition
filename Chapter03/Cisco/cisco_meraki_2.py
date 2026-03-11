#!/usr/bin/env python3
import requests
import pprint

myheaders={'X-Cisco-Meraki-API-Key': '1106ae045835127e04925c5a224cec0f07504121'}
orgId = '1649105'
url = 'https://dashboard.meraki.com/api/v1/organizations/' + orgId + '/networks'
response = requests.get(url, headers=myheaders, verify=False)
pprint.pprint(response.json())
