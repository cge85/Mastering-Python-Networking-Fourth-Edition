#!/usr/bin/env python3

import pexpect

devices = {'iosv-1': {'prompt': 'r1#', 'ip': '10.10.10.101'}}
username = 'admin'
password = 'cisco'

for device in devices.keys():
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username:')
    child.sendline(username)
    child.expect('Password:')
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('sh ip access-lists permit_snmp | i 192.168.0.8')
    child.expect(device_prompt)
    output = child.before
    print(str(output).split('(')[1].split()[0])
    child.sendline('exit')
