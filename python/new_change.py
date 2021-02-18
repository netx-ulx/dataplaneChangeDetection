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

def thresh(error_sketch,T):
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

    TA = T * sqrt(error_sketch.ESTIMATEF2())
    return TA

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

    #print("Optimized!")

    keys = set() #set used to save the keys that appeared during the epoch
    cur_epoch = None #current epoch
    forecast_sketch1 = KAry_Sketch(kary_depth,kary_width)
    forecast_sketch2 = KAry_Sketch(kary_depth,kary_width)
    error_sketch = KAry_Sketch(kary_depth,kary_width)
    control_sketch = KAry_Sketch(kary_depth,kary_width)
    control = False
    threshold = None
    col = 0

    first_epoch = True
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
            if first_epoch:
                first_epoch = False
            else:
                if control:
                    for col in range(0,kary_width):
                        for i in range(0,kary_depth):
                            #control is 0, change to 1
                            if control_sketch.sketch[i][col] != 1:
                                forecast_sketch2.sketch[i][col] = (1-alpha)*forecast_sketch1.sketch[i][col]
                                error_sketch.sketch[i][col] = - forecast_sketch1.sketch[i][col]
                                control_sketch.sketch[i][col] = 1
                else:
                    for col in range(0,kary_width):
                        for i in range(0,kary_depth):
                            #control is 0, change to 1
                            if control_sketch.sketch[i][col] != 0:
                                forecast_sketch1.sketch[i][col] = (1-alpha)*forecast_sketch2.sketch[i][col]
                                error_sketch.sketch[i][col] = - forecast_sketch2.sketch[i][col]
                                control_sketch.sketch[i][col] = 0
                #perform change detection
                threshold = thresh(error_sketch,T)

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

            control = not control
            col = 0
            cur_epoch = packet["time"]
            keys.clear()

        if first_epoch:
            forecast_sketch1.UPDATE(packet['key'],10,hash_func)
        else:
            #forecast_sketch1 is the Sf(t), forecast_sketch2 is the Sf(t+1)
            if control:
                result, buckets = forecast_sketch1.QUERY(packet['key'],hash_func)

                for i in range(0,kary_depth):
                    #control is 0, change to 1
                    if control_sketch.sketch[i][buckets[i]] != 1:
                        forecast_sketch2.sketch[i][buckets[i]] = 10*alpha + 10*(1-alpha)*(result[i]//10)
                        error_sketch.sketch[i][buckets[i]] = 10 - result[i]
                        control_sketch.sketch[i][buckets[i]] = 1
                    else:
                        forecast_sketch2.sketch[i][buckets[i]] = forecast_sketch2.sketch[i][buckets[i]] + 10*alpha
                        error_sketch.sketch[i][buckets[i]] = error_sketch.sketch[i][buckets[i]] + 10
                    
                #copy one more
                if col < kary_width:
                    for i in range(0,kary_depth):
                        #control is 0, change to 1
                        if control_sketch.sketch[i][col] != 1:
                            forecast_sketch2.sketch[i][col] = 10*(1-alpha)*(forecast_sketch1.sketch[i][col]//10)
                            error_sketch.sketch[i][col] = - forecast_sketch1.sketch[i][col]
                            control_sketch.sketch[i][col] = 1
                col = col + 1
            else:
                result, buckets = forecast_sketch2.QUERY(packet['key'],hash_func)
                
                for i in range(0,kary_depth):
                    #control is 1, change to 0
                    if control_sketch.sketch[i][buckets[i]] != 0:
                        forecast_sketch1.sketch[i][buckets[i]] = 10*alpha + 10*(1-alpha)*(result[i]//10)
                        error_sketch.sketch[i][buckets[i]] = 10 - result[i]
                        control_sketch.sketch[i][buckets[i]] = 0
                    else:
                        forecast_sketch1.sketch[i][buckets[i]] = forecast_sketch1.sketch[i][buckets[i]] + 10*alpha
                        error_sketch.sketch[i][buckets[i]] = error_sketch.sketch[i][buckets[i]] + 10
                #copy one more
                if col < kary_width:
                    for i in range(0,kary_depth):
                        #control is 1, change to 0
                        if control_sketch.sketch[i][col] != 0:
                            forecast_sketch1.sketch[i][col] = 10*(1-alpha)*(forecast_sketch2.sketch[i][col]//10)
                            error_sketch.sketch[i][col] = - forecast_sketch2.sketch[i][col]
                            control_sketch.sketch[i][col] = 0
                col = col + 1
            #STORE KEY FOR CHANGE DETECTION
            keys.add(packet["key"])

    return complex_result, result