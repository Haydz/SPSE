#! /usr/bin/env python

import sys
from scapy.all import srp,Ether,ARP,conf
if len(sys.argv) !=2:
    print "Usage: arping2text <net> |n eg : arping2text 192.168.1.0/24"
    sys.exit(1)

conf.verb=0
ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1]),timeout=2)

print r"\begin{tabular}{|1|1|}"
print r"\hline"
print"MAC & IP\\"
for snd,rcv in ans:
    print rcv.sprintf(r"%Ether.src% & %ARP.psrc%\\")
print r"\hline"
print r"\end{tabular}"
