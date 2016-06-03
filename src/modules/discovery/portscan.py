import nmap
from netaddr import IPNetwork

def myScann():
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