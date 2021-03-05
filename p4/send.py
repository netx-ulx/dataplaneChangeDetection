#!/usr/bin/env python2

from scapy.all import *
from scapy.utils import rdpcap
import sys

if len(sys.argv) < 2:
    print("Usage: ./send.py [Trace path]")
else:
    count=0
    pkts=PcapReader(sys.argv[1])
    for pkt in pkts:
        #input("Enter")
        sendp(pkt, iface="veth2")
        count+=1
        print(count)
