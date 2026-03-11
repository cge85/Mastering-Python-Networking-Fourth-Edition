#!/usr/bin/env python3

from ncclient import manager
import xml.dom.minidom

host = "192.168.0.33"
username = "admin"
password = "cisco"
port = 830

yang_file = "cisco_yang_1_interfaces.xml"

conn = manager.connect(
    host=host, 
    port=port, 
    username=username, 
    password=password, 
    hostkey_verify=False, 
    device_params={'name': 'iosxe'}, 
    allow_agent=False, 
    look_for_keys=False
    )

with open(yang_file) as f: 
    output = conn.get_config(source='running', filter=('subtree', f.read()))

print(xml.dom.minidom.parseString(output.xml).toprettyxml())