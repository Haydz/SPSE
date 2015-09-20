#! /usr/bin/env python
import sys
from scapy.all import sr1,IP,ICMP

p=sr1(IP(dst="google.com")/ICMP())
if p:
    p.show()