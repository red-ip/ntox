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
import nmap
from netaddr import IPNetwork


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

    def start_nmap(self):
        nm = nmap.PortScanner()             # instantiate nmap.PortScanner object
        print('----------------------------------------------------')
        # If you want to do a pingsweep on network 192.168.1.0/24:
        nm.scan(hosts='192.168.180.0/24', arguments='-sP 161')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host, status in hosts_list:
            print('{0}:{1}'.format(host, status))


        print('----------------------------------------------------')
        # Asynchronous usage of PortScannerAsync
        nma = nmap.PortScannerAsync()
        def callback_result(host, scan_result):
            print('------------------')
            print(host, scan_result)
        nma.scan(hosts='192.168.100.0/24', arguments='-sP', callback=callback_result)
        while nma.still_scanning():
            print("Waiting ...")
            nma.wait(2)   # you can do whatever you want but I choose to wait after the end of the scan

    def my_scann(self):
        nm = nmap.PortScanner()
        for loop_1 in IPNetwork('192.168.100.0/24'):
            (nm.scan(loop_1.format(), '22')).get('state')
            try:
                state = (nm[loop_1.format()]['tcp'][22]['state'])
                if state == "open":
                    print(loop_1, " IS ", state)
                elif state == "closed":
                    pass
            except KeyError as e:
                print(e)