import mmh3
import string
from copy import deepcopy
from statistics import median
from math import sqrt
import getopt, sys
import binascii
from kary_sketch import *
from forecast_module import MA,EWMA,NSHW
from decimal import Decimal

def extract(key_format,packet):
    key = []
    for elem in key_format:
        if elem == "src":
            key.append(packet["key"]["src"])
        if elem == "dst":
            key.append(packet["key"]["dst"])
        if elem == "sport":
            key.append(packet["key"]["sport"])
        if elem == "dport":
            key.append(packet["key"]["dport"])
        if elem == "proto":
            key.append(packet["key"]["proto"])
    
    new_packet = {
        "key": tuple(key),
        "val": packet["val"],
        "time": packet["time"]
    }
    return new_packet

def change(forecast_sketch,observed_sketch,T):
    """Constructs the forecast error sketch and chooses an alarm threshold, based on the second moment of the forecast error sketch.

    Parameters
    ----------
    forecast_sketch : KAry_Sketch
        A forecast sketch
    observed_sketch : KAry_Sketch
        An observed sketch

    Returns
    -------
    KAry_Sketch
        The forecast error sketch
    dict
        The packet with a key, the time of the packet, and its size.
    """

    depth = len(observed_sketch.sketch)
    width = len(observed_sketch.sketch[0])

    new_error_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            new_error_sketch.sketch[i][j] = observed_sketch.sketch[i][j] - forecast_sketch.sketch[i][j]
    TA = T * sqrt(new_error_sketch.ESTIMATEF2())
    return new_error_sketch, TA

def main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets):
    """Processes all packets running forecasting models and change detection mechanisms for every epoch.

    Parameters
    ----------
    kary_depth : int
        The depth of the K-ary Sketch
    kary_width : int
        The width of the K-ary Sketch
    kary_epoch : float
        The size of a K-ary Epoch
    alpha : float
        Alpha to be used by the EWMA and NSHW
    beta : float
        Beta to be used by the NSHW
    T : float
        The threshold to be used for change detection
    s : int
        Number of past sketches to be saved
    hash_func : string
        The hash function used for updating the sketch
    forecasting_model : string
        The forecasting model used for forecasting
    key_format : list
        A list of key options to be used
    packets : RAW Packets
        All packets from Scapy

    """

    #print("Original!")

    keys = set() #set used to save the keys that appeared during the epoch
    cur_epoch = None #current epoch
    forecast_sketch = None
    error_sketch = None
    threshold = None

    trend_sketch = None #For use only with NSHW
    smoothing_sketch = None #For use only with NSHW
    
    #initialize sketch list
    sketch_list = [] #keeps current sketch [-1] and s past sketches
    for _ in range(0,s+1):
        sketch_list.append(KAry_Sketch(kary_depth,kary_width))

    control = 1
    complex_result = []
    result = []
    for pkt in packets:
        #EXTRACT PACKET FIELDS
        packet = extract(key_format,pkt)
        
        #first epoch starts at the time of the first packet
        if cur_epoch == None:
            cur_epoch = packet["time"]
        #Check if new packet is outside the current epoch
        if cur_epoch < packet["time"] - kary_epoch:
            part_result = None
            #Only perform change detection if t >= 2
            if control > 1:
                #FORECASTING
                if forecasting_model == "ma":
                    #print("Using MA")
                    forecast_sketch = MA(sketch_list,s)
                elif forecasting_model == "ewma":
                    #print("Using EWMA")
                    forecast_sketch = EWMA(forecast_sketch,sketch_list[-2],alpha)
                elif forecasting_model == "nshw":
                    #print("Using NSHW")
                    forecast_sketch, smoothing_sketch, trend_sketch = NSHW(forecast_sketch,sketch_list[-2],sketch_list[-1],trend_sketch,smoothing_sketch,alpha,beta)

                #CHANGE DETECTION
                error_sketch, threshold = change(forecast_sketch,sketch_list[-1],T)
                #print("Threshold =", threshold, "Time:",cur_epoch)

                part_result = {
                    "epoch": [threshold,cur_epoch],
                    "res": None,
                    "TN": 0,
                }

                complex_res = []
                res = []
                #error_sketch.SHOW()
                for key in keys:
                    estimate = error_sketch.ESTIMATE(key,hash_func)
                    if estimate > threshold:
                        complex_res.append(key)
                        res.append(key)
                        #print("Change detected for:", key, "with estimate:", estimate)
                part_result["res"] = complex_res
                part_result["numKeys"] = len(keys)
                result.append(res)
                complex_result.append(part_result)

            #print("Changing epoch ")
            cur_epoch = packet["time"]

            if control == 1:
                control = 2

            #shift left, deleting first [0]
            for i in range(0,s):
                sketch_list[i] = deepcopy(sketch_list[i+1])

            sketch_list[-1].RESET()
            keys.clear()

        #UPDATE SKETCH
        sketch_list[-1].UPDATE(packet["key"],1,hash_func)

        #STORE KEY FOR CHANGE DETECTION
        keys.add(packet["key"])

    return complex_result, result