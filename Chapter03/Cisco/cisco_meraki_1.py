#!/usr/bin/env python3
import requests
import pprint

myheaders={'X-Cisco-Meraki-API-Key': '1106ae045835127e04925c5a224cec0f07504121'}
url = 'https://dashboard.meraki.com/api/v1/organizations'
response = requests.get(url, headers=myheaders, verify=False)

# Debug regels:
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}") 

if response.ok:
    pprint.pprint(response.json())
else:
    print("Er ging iets mis met de aanvraag.")


