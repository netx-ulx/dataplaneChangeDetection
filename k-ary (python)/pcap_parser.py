from scapy.all import *
import string

def expand(x):
     yield x.name
     while x.payload:
         x = x.payload
         yield x.name

def extract(key_format,packet):
    """Extracts relevant information from a packet.
    Parameters
    ----------
    key_format : list
        A list of key options
    packet : RAW Packet
        A packet from Scapy
    Returns
    -------
    KAry_Sketch
        The forecast error sketch
    float
        The threshold
    """
    
    src = None
    dst = None
    for elem in key_format:
        if elem == "src":
            if IP in packet:
                src = packet[IP].src
        if elem == "dst":
            if IP in packet:
                dst = packet[IP].dst
        if elem == "sport":
            try:
                sport = packet.sport
            except:
                sport = 0
        if elem == "dport":
            try:
                dport = packet.dport
            except:
                dport = 0
        if elem == "proto":
            try:
                lst = list(filter(lambda x: x != 'Raw', list(expand(packet))))
                lst1 = list(filter(lambda x: x != 'Padding', lst))
                proto = lst1[-1]
            except:
                proto = None
    try:
        value = packet.len
    except:
        value = len(packet)
        
    time = packet.time

    key = {
        "src": src,
        "dst": dst,
        "sport": str(sport),
        "dport": str(dport),
        "proto": str(proto)
    }
    
    packet = {
        "key": key,
        "val": value,
        "time": time
    }
    return packet

def parse(path):
    raw_packets = PcapReader(path)
    packets = []
    for pkt in raw_packets:
        packets.append(extract(["src","dst","sport","dport","proto"],pkt))
    return packets