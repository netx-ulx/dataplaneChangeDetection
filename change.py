from scapy.all import rdpcap, copy, PcapReader
import mmh3
import string
from statistics import median
from math import sqrt
import getopt, sys
import binascii
from kary_sketch import *
from forecast_module import MA,EWMA,NSHW

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
    float
        The threshold
    """

    depth = len(observed_sketch.sketch)
    width = len(observed_sketch.sketch[0])

    new_error_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            new_error_sketch.sketch[i][j] = observed_sketch.sketch[i][j] - forecast_sketch.sketch[i][j]
    TA = T * sqrt(new_error_sketch.ESTIMATEF2())
    return new_error_sketch, TA

def main():
    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    kary_epoch = 0.1 #seconds per epoch
    path = "traces/trace1.pcap" #path for the pcap file
    alpha = 0.7 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    T = 0.1 #threshold used by the change detection module
    s = 1 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting mdoel to be used by the forecasting module
    key_format = ["src","dst","dport","sport","proto"] #format of the key, contains all possible options by default

    supported_hashes = ["murmur3","crc32"]
    supported_models = ["ma","ewma","nshw"]
    keys = set() #set used to save the keys that appeared during the epoch
    cur_epoch = None #current epoch

    #-------------------------------------------- PROCESS INPUT --------------------------------------------#
    short_options = "a:d:e:f:h:k:p:s:t:w:"                                                                                                                                         
    long_options = ["help", "alpha=", "depth=", "epoch=", "fmodel=", "hash=", "key=", "path=", "saved=", "thresh=", "width="]
    # Get full command-line arguments but the first
    argument_list = sys.argv[1:]

    try:
        arguments, _ = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)

    # Evaluate given options
    for current_argument, current_value in arguments:
        if current_argument in ("-a", "--alpha"):
            print("Updating alpha to", current_value)
            alpha = float(current_value)
        elif current_argument in ("-d", "--depth"):
            print("Updating depth to", current_value)
            kary_depth = int(current_value)
        elif current_argument in ("-e", "--epoch"):
            print("Updating epoch to", current_value)
            kary_epoch = float(current_value)
        elif current_argument in ("-f", "--fmodel"):
            if current_value in supported_models:
                print("Updating forecasting model to", current_value)
                forecasting_model = current_value
            else:
                print("Forecasting Model:", current_value, "not supported.")
                sys.exit(2)
        elif current_argument in ("-h", "--hash"):
            if current_value in supported_hashes:
                print("Updating Hash function to", current_value)
                hash_func = current_value
            else:
                print("Hash Function:", current_value, "not supported.")
                sys.exit(2)
        elif current_argument in ("-k", "--key"):
            print("Updating key to", current_value)
            for value in current_value.split(","):
                if value not in key_format:
                    print("Key value:", value, "not supported.")
                    sys.exit(2)
            key_format = current_value.split(",")
        elif current_argument in ("-p", "--path"):
            print("Updating path to", current_value)
            path = current_value
        elif current_argument in ("-s", "--saved"):
            print("Updating number of past sketches saved to", current_value)
            s = int(current_value)
        elif current_argument in ("-t", "--thresh"):
            print("Updating Threshold to", current_value)
            T = float(current_value)
        elif current_argument in ("-w", "--width"):
            print("Updating width to", current_value)
            kary_width = int(current_value)
        elif current_argument in ("--help"):
            print  ("------------------------------------------------------------------------------------\n",
                    "long argument   short argument  value               default                         \n",
                    "------------------------------------------------------------------------------------\n",
                    "--alpha          -a              positive float      0.7                            \n",
                    "--depth          -d              positive integer    5                              \n",
                    "--epoch          -e              positive float      0.1                            \n",
                    "--fmodel         -f              string              ewma                           \n",
                    "--hash           -h              string              murmur3                        \n",
                    "--key            -k              opts...             src,dst,sport,dport,proto      \n",
                    "--path           -p              string              traces/trace1.pcap             \n",
                    "--saved          -s              positive integer    1                              \n",
                    "--thresh         -t              positive float      0.1                            \n",
                    "--width          -w              positive integer    5462                           \n",
                    "--------------------------------------------------------------------------------------")
            sys.exit(2)
                                                                                                        
    #----------------------------------------------- | | -----------------------------------------------#

    forecast_sketch = None
    error_sketch = None
    threshold = None

    trend_sketch = None #For use only with NSHW
    smoothing_sketch = None #For use only with NSHW
    
    #initialize sketch list
    sketch_list = [] #keeps current sketch [-1] and s past sketches
    for _ in range(0,s+1):
        sketch_list.append(KAry_Sketch(kary_depth,kary_width))

    packets = PcapReader(path)

    control = 1

    for packet in packets:
        #-------------------------------------------- EXTRACT PACKET FIELDS --------------------------------------------#
        key = []
        for elem in key_format:
            if elem == "src":
                src = packet.src
                key.append(src)
            if elem == "dst":
                dst = packet.dst
                key.append(dst)
            if elem == "sport":
                try:
                    sport = packet.sport
                except:
                    sport = 0
                key.append(str(sport))
            if elem == "dport":
                try:
                    dport = packet.dport
                except:
                    dport = 0
                key.append(str(dport))
            if elem == "proto":
                try:
                    proto = packet.proto
                except:
                    proto = 0
                key.append(str(proto))

        try:
            value = packet.len
        except:
            value = len(packet)
            
        time = packet.time
        
        packet = {
            "key": tuple(key),
            "val": value,
            "time": time
        }
        #----------------------------------------------------- | | -----------------------------------------------------#
        
        #first epoch starts at the time of the first packet
        if cur_epoch == None:
            cur_epoch = packet["time"]

        #Check if new packet is outside the current epoch
        if cur_epoch < packet["time"] - kary_epoch:
            #Only perform change detection if t >= 2
            if control > 1:
                #FORECASTING
                if forecasting_model == "ma":
                    print("Using MA")
                    forecast_sketch = MA(sketch_list,s)
                elif forecasting_model == "ewma":
                    print("Using EWMA")
                    forecast_sketch = EWMA(forecast_sketch,sketch_list[-2],alpha)
                elif forecasting_model == "nshw":
                    print("Using NSHW")
                    forecast_sketch = NSHW(forecast_sketch,sketch_list[-2],sketch_list[-1],trend_sketch,smoothing_sketch,alpha,beta)

                #CHANGE DETECTION
                error_sketch, threshold = change(forecast_sketch,sketch_list[-1],T)
                print("Threshold =", threshold, "Time:",cur_epoch)
                #error_sketch.SHOW()
                for key in keys:
                    estimate = error_sketch.ESTIMATE(key,hash_func)
                    if estimate  > threshold:
                        print("Change detected for:", key, "with estimate:", estimate)

            print("Changing epoch ")
            cur_epoch = packet["time"]

            if control == 1:
                control = 2

            #shift left, deleting first [0]
            for i in range(0,s):
                sketch_list[i] = copy.deepcopy(sketch_list[i+1])

            sketch_list[-1].RESET()
            keys.clear()

        #UPDATE SKETCH
        sketch_list[-1].UPDATE(packet["key"],packet["val"],hash_func)
        #sketch_list[-1].UPDATE(packet["key"],1)

        #STORE KEY FOR CHANGE DETECTION
        keys.add(packet["key"])
    
if __name__ == "__main__":
  main()