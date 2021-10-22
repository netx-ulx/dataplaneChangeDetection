import string
from copy import deepcopy
from statistics import median
from math import sqrt
import getopt, sys
import binascii
from kary_sketch import *
from forecast_module import MA,EWMA,EWMA_approx,NSHW
from decimal import Decimal

def extract(key_format,packet):
    key = []
    for elem in key_format:
        if elem == "src":
            key.append(packet["key"]["src"])
        if elem == "dst":
            key.append(packet["key"]["dst"])
        if elem == "dport":
            key.append(packet["key"]["dport"])
        if elem == "sport":
            key.append(packet["key"]["sport"])
        if elem == "proto":
            key.append(packet["key"]["proto"])
    
    new_packet = {
        "key": tuple(key),
        "val": packet["val"],
        "time": packet["time"]
    }

    if any(v is None for v in key):
        return None

    return new_packet

def change(forecast_sketch,observed_sketch,T):
    """Constructs the forecast error sketch and chooses an alarm threshold, based on the second moment of the forecast error sketch.

    Parameters
    ----------
    forecast_sketch : KAry_Sketch
        A forecast sketch
    observed_sketch : KAry_Sketch
        An observed sketch
    T : float
        The threshold

    Returns
    -------
    KAry_Sketch
        The forecast error sketch
    TA 
        The application threshold
    """

    depth = len(observed_sketch.sketch)
    width = len(observed_sketch.sketch[0])

    new_error_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            new_error_sketch.sketch[i][j] = observed_sketch.sketch[i][j] - forecast_sketch.sketch[i][j]
    TA = T * sqrt(new_error_sketch.ESTIMATEF2())
    return new_error_sketch, TA/10

def removeDuplicates(lst):
      
    return list(set([i for i in lst]))

def main_cycle(kary_depth,kary_width,kary_epoch,epoch_control,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets,mv,approx):
    """Processes all packets running forecasting models and change detection mechanisms for every epoch.

    Parameters
    ----------
    kary_depth : int
        The depth of the K-ary Sketch
    kary_width : int
        The width of the K-ary Sketch
    kary_epoch : int
        The num of packets per epoch
    epoch_control : str
        The epoch control type (time or num packets)
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
    mv : bool
        flag to use the mjrty from the mv sketch
    approx : bool
        flag to use the approximations from the p4 version

    """

    epoch_counter = -1 #epoch counter
    epoch_start_time = 0
    forecast_sketch = None
    error_sketch = None
    threshold = None
    cur_epoch = None

    trend_sketch = None #For use only with NSHW
    smoothing_sketch = None #For use only with NSHW
    
    #initialize sketch list
    sketch_list = [] #keeps current sketch [-1] and s past sketches
    for _ in range(0,s+1):
        sketch_list.append(KAry_Sketch(kary_depth,kary_width,mv))

    control = 1
    complex_result = []
    result = []
    num_packets = 0
    for pkt in packets:
        num_packets = num_packets + 1
        #EXTRACT PACKET FIELDS
        packet = extract(key_format,pkt)
        if packet == None:
            continue


        # EPOCH CONTROL
        #first epoch starts at the time of the first packet
        if cur_epoch == None:
            if epoch_control == "time":
                cur_epoch = packet["time"]
            else:
                cur_epoch = 0
            epoch_start_time = packet["time"]

        new_epoch = 0
        if epoch_control == "time":
            if cur_epoch < packet["time"] - kary_epoch:
                new_epoch = 1
                cur_epoch = cur_epoch + kary_epoch
        else:
            if cur_epoch >= kary_epoch:
                new_epoch = 1
                cur_epoch = 0

        #Check if new packet is outside the current epoch
        if new_epoch == 1:
            epoch_counter = epoch_counter + 1
            part_result = None
            #Only perform change detection if t >= 2
            if control > 1:
                #FORECASTING
                if forecasting_model == "ma":
                    forecast_sketch = MA(sketch_list,s)
                elif forecasting_model == "ewma" and approx:
                    forecast_sketch = EWMA_approx(forecast_sketch,sketch_list[-2],alpha)
                elif forecasting_model == "ewma":
                    forecast_sketch = EWMA(forecast_sketch,sketch_list[-2],alpha) 
                elif forecasting_model == "nshw":
                    forecast_sketch, smoothing_sketch, trend_sketch = NSHW(forecast_sketch,sketch_list[-2],sketch_list[-1],trend_sketch,smoothing_sketch,alpha,beta)

                #CHANGE DETECTION
                error_sketch, threshold = change(forecast_sketch,sketch_list[-1],T)

                complex_res = []
                res = []
                keys = []
                
                if mv:
                    for row in sketch_list[-1].keys:
                        for key in row:
                            keys.append(key)
                else:
                    keys = sketch_list[-1].keys

                keys = removeDuplicates(keys)
                if (None,None) in keys:
                    keys.remove((None,None))

                part_result = {
                    "epoch": [threshold,(epoch_counter,epoch_start_time),packet["time"],num_packets,len(keys)],
                    "res": None,
                    "TN": 0,
                }

                for key in keys:
                    if not any(v is None for v in key):
                        estimate = error_sketch.ESTIMATE(key,hash_func)/10
                        #print(estimate)
                        if estimate > threshold:
                            complex_res.append(key + (str(estimate),))
                            res.append(key)
                            #print("Change detected for:", key, "with estimate:", estimate)

                part_result["res"] = complex_res
                part_result["numKeys"] = len(keys)
                result.append(res)
                complex_result.append(part_result)

            if control == 1:
                control = 2

            #shift left, deleting first [0]
            for i in range(0,s):
                sketch_list[i] = deepcopy(sketch_list[i+1])

            epoch_start_time = epoch_start_time + kary_epoch
            
            sketch_list[-1].RESET()
            
        #UPDATE SKETCH
        sketch_list[-1].UPDATE(packet["key"],10,hash_func)
        if epoch_control != "time":
            cur_epoch = cur_epoch + 1

    return complex_result, result