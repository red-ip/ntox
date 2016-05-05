# -*- encoding: utf-8 -*-

"""
ntox.py
===================

(C) RedIP GmbH, 2016 <info@red-ip.de>
"""
from pysnmp.entity.rfc3413.oneliner import cmdgen
import ipaddress
from threading import Thread
import src.modules.discovery.switch as myswitch

class Discover:
    network = None
    community_string = "public"
    snmp_list = []
    threads = []
    devices = []
    vendors = ["Avaya", "Cisco", "Meraki", "Nortel", "Juniper"]
    counter = 1

    def __init__(self, subnet, cidr):
        self.network = ipaddress.ip_network(str(subnet)+'/'+str(cidr))

#TODO: write a generic function for device fingerprinting (Servers, switches, routers etc.)
    def fingerprint(self, sysDescr):
        for vendor in self.vendors:
            if vendor in sysDescr and "Switch" in sysDescr:
                return vendor


    def snmp_get_next(self,host,community_string):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community_string),
                cmdgen.UdpTransportTarget((str(host), 161), timeout=0.1, retries=0),
                '1.3.6.1.2.1.1.1.0',
        )
        # Check for errors and print out results
        self.counter = self.counter+1
        if not (errorIndication):
            if not (errorStatus):
                for name, val in varBinds:
                    self.snmp_list.append((host, val.prettyPrint()))


    # Start check for each network device in a new thread
    def start_discover(self):
        network_list = list(self.network.hosts())
        for host in network_list:
            t = Thread(target=self.snmp_get_next, args=(host, 'public'))
            t.start()
            self.threads.append(t)

        # Wait for all threads to finish
        for x in self.threads:
            x.join()

        for snmp_dev in self.snmp_list:
            tmp_switch = myswitch.Switch(str(self.fingerprint(str(snmp_dev))), str(snmp_dev[0]))
            #TODO: Get credentials from somewhere
            tmp_switch.set_login('RO', 'coselose!#')
            self.devices.append(tmp_switch)