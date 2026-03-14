#!/usr/bin/env python3

import json
import pyeapi

class my_switch():
    
    def __init__(self, config_file_location, device):
        # loads the config file 
        pyeapi.client.load_config(config_file_location)
        self.node = pyeapi.connect_to(device)
        self.hostname = self.node.enable('show hostname')[0]['result']['hostname']
        self.running_config = self.node.enable('show running-config')

    def create_vlan(self, vlan_number, vlan_name):
        vlans = self.node.api('vlans')
        vlans.create(vlan_number)
        vlans.set_name(vlan_number, vlan_name)

s1 = my_switch('~/.eapi.conf', 'nyc-edg-r4')
s1.create_vlan(100,'TEST_VLAN')

output = {
    'hostname': s1.hostname,
    'running_config': s1.running_config,
    'vlans': s1.node.api('vlans').getall()
}

print(json.dumps(output, indent=2, sort_keys=True))