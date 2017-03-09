#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

# Integration of the external libs
script_path = "../external/"
sys.path.append(os.path.abspath(script_path))

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import xmlrpc.client as xmlrpclib


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    s = xmlrpclib.ServerProxy('http://192.168.180.84:8099')
    results = s.scan(targets, options)
    return results


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                str(serv.port),
                serv.protocol,
                serv.state,
                serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
    print(nmap_report.summary)


if __name__ == "__main__":
    report = do_scan("192.168.100.10", "-sV")
    if report:
        print_scan(report)
    else:
        print("No results returned")
