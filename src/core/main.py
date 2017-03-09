# -*- encoding: utf-8 -*-
"""
ntox.py
===================

(C) RedIP GmbH, 2016 <info@red-ip.de>
"""

import sys
import os

# Integration of the external libs
script_path = "../external/"
sys.path.append(os.path.abspath(script_path))
from netmiko import ConnectHandler

switch_avaya = {
    'device_type': 'avaya_ers',
    'ip': '172.16.30.10',
    'use_keys': True,
    'key_file': '/Volumes/JKSKEY/RemoteLinkEndpoint/rle490005/rle490005portaccess1',
    'username': 'portaccess1:port1',
    'password': '1234!#',
}

net_connect = ConnectHandler(**switch_avaya)
print("----------")
net_connect.find_prompt()
print("----------")

output = net_connect.send_command("RO")
print(output)
output = net_connect.send_command("coselose#")
print(output)
print("alles ok")
