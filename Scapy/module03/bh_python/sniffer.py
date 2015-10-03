__author__ = 'root'

from scapy.all import *

#our packet call back
def packet_callback(packet):
    print packet.show()

#fire up sniffer with ocount of 1.

sniff(prn=packet_callback,count=1)
