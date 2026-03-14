#!/usr/bin/env python

import vymgmt

vyos = vymgmt.Router('192.168.0.24', 'vyos', password='vyos')
vyos.login()
vyos.configure()
vyos.set("system domain-name networkautomationnerds.net")
vyos.commit()
vyos.save()

raw_output = vyos.run_op_mode_command('show configuration | match domain-name')

domain_name = ""
for line in raw_output.splitlines():
    if 'domain-name' in line:
        domain_name = line.split()[1]

print(domain_name)

vyos.exit()
vyos.logout()