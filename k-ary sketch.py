from scapy.all import rdpcap, copy, PcapReader
import mmh3
import string
from statistics import median
from math import sqrt
import getopt, sys

class KAry_Sketch:
    """
    A class used to represent a K-ary Sketch structure

    Attributes
    ----------
    depth : int 
        The depth of the sketch: number of rows
    width : int
        The width of the sketch: number of buckets in each row

    Methods
    -------
    UPDATE(key,value)
        Updates the sketch with the value for a given key
    ESTIMATE(key)
        Estimates the value for a given key
    sum()
        Calculates the sum of all values in the sketch
    ESTIMATEF2()
        Calculates the estimated second moment (F2) of the sketch
    SHOW()
        Prints the sketch matrix
    RESET()
        Resets the sketch by zeroing the sketch matrix
    """

    def __init__(self,depth,width):
        """
        Parameters
        ----------
        depth : int 
            The depth of the sketch: number of rows
        width : int
            The width of the sketch: number of buckets in each row
        """
        
        self.depth = depth
        self.width = width
        self.sketch = []
        self.seeds = []
        #initialize the sketch structure
        for i in range(0,depth):
            self.sketch.append([])
            for _ in range(0,width):
                self.sketch[i].append(0)
        #initialize the hash seeds for each row
        for i in range(0,depth):
            self.seeds.append(mmh3.hash64("K-ARY SKETCH",i)[0])

    def UPDATE(self,key,value):
        """Updates the sketch with the value for a given key

        Parameters
        ----------
        key : tuple 
            A five-tuple key (src,dst,sport,dport,proto)
        value : float 
            The value to be updated
        """

        for i in range(0,self.depth):
            bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            self.sketch[i][bucket] = self.sketch[i][bucket] + value

    def ESTIMATE(self,key):
        """Estimates the value for a given key

        Parameters
        ----------
        key : tuple 
            A five-tuple key (src,dst,sport,dport,proto)
        
        Returns
        -------
        float
            The estimated value for a given key
        """

        result = []
        for i in range(0,self.depth):
            bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            result.append( (self.sketch[i][bucket] - (self.sum()/self.width)) / (1 - (1/self.width)))
        return median(result)

    def sum(self):
        """Calculates the sum of all values in the sketch
        
        Returns
        -------
        float
            The sum of all values in the sketch
        """

        return sum(self.sketch[0])

    def ESTIMATEF2(self):
        """Calculates the estimated second moment (F2) of the sketch
        
        Returns
        -------
        float
            The estimated F2 of the sketch
        """

        result = []
        for i in range(0,self.depth):
            aux = 0
            for j in range(0,self.width):
                aux = aux + (self.sketch[i][j]**2) 
            result.append(((self.width/(self.width-1))*aux) - ((1/(self.width-1))*(self.sum()**2)))
        return median(result)

    def COMBINE(self,sketch):
        #TODO
        pass

    def SHOW(self):
        """Prints the sketch matrix"""

        print(self.sketch)

    def RESET(self):
        """Resets the sketch by zeroing the sketch matrix"""

        for i in range(0,self.depth):
            for j in range(0,self.width):
                self.sketch[i][j] = 0

def MA(sketch_list,w):
    """Uses the Moving Average Model to build the forecast sketch from the list of sketches observed in the past

    Parameters
    ----------
    sketch_list : list
        A list of observed sketches
    w : int
        number of past sketches saved for forecast

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(sketch_list[0].sketch)
    width = len(sketch_list[0].sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            _sum = 0
            for p in range(2,w+2):
                _sum = _sum + sketch_list[-p].sketch[i][j]
            new_forecast_sketch.sketch[i][j] = _sum / w
    return new_forecast_sketch

def SMA(forecast_sketch,sketch_list,w,weigths):
    """Uses the S-shaped Moving Average Model to build the forecast sketch from the list of sketches observed in the past

    Parameters
    ----------
    forecast_sketch : KAry_Sketch
        A forecast sketch
    sketch_list : list
        A list of observed sketches
    w : int
        The number of past sketches saved for forecast
    weigths: list
        A list of weights given to each past epoch

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(sketch_list[0].sketch)
    width = len(sketch_list[0].sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
        for j in range(0,width):
            _sum = 0
            for p in range(2,w+2):
                _sum = _sum + (weigths[p-2] * sketch_list[-p].sketch[i][j])
            new_forecast_sketch.sketch[i][j] = _sum / sum(weigths)
    return new_forecast_sketch

def EWMA(previous_forecast_sketch,previous_observed_sketch,alpha):
    """Uses the Exponentially Weighted Moving Average Model to build the forecast sketch from the previous forecast and observed sketch

    Parameters
    ----------
    forecast_sketch : KAry_Sketch
        A forecast sketch
    observed_sketch : KAry_Sketch
        An observed sketch
    alpha : float
        The alpha value to be used by the EWMA

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(previous_observed_sketch.sketch)
    width = len(previous_observed_sketch.sketch[0])
    new_forecast_sketch = KAry_Sketch(depth,width)
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                new_forecast_sketch.sketch[i][j] = (alpha*previous_observed_sketch.sketch[i][j]) + ((1-alpha)*previous_forecast_sketch.sketch[i][j])
        return new_forecast_sketch
    else:
        return copy.deepcopy(previous_observed_sketch)

def NSHW(previous_forecast_sketch,previous_observed_sketch,observed_sketch,previous_trend,previous_smoothing,alpha,beta):
    """Uses the Non-Seasonal Holt-Winters Model to build the forecast sketch from the previous forecast, observed sketch, trend and smoothing

    Parameters
    ----------
    previous_forecast_sketch : KAry_Sketch
        A forecast sketch
    previous_observed_sketch : KAry_Sketch
        An observed sketch
    observed_sketch : KAry_Sketch
        An observed sketch
    previous_trend : KAry_Sketch
        The previous trend sketch
    previous_smoothing : KAry_Sketch
        The previous smoothing sketch
    alpha : float
        The alpha value to be used by the EWMA
    beta : float
        The beta value to be used by the EWMA
smoothing
    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    depth = len(previous_observed_sketch.sketch)
    width = len(previous_observed_sketch.sketch[0])
    smoothing_sketch = KAry_Sketch(depth,width)
    trend_sketch = KAry_Sketch(depth,width)

    #smoothing
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                smoothing_sketch.sketch[i][j] = (alpha*previous_observed_sketch.sketch[i][j]) + ((1-alpha)*previous_forecast_sketch.sketch[i][j])
    else:
        smoothing_sketch = copy.deepcopy(previous_observed_sketch)

    #trend
    if previous_forecast_sketch != None:
        for i in range(0,depth):
            for j in range(0,width):
                trend_sketch.sketch[i][j] = (beta*(smoothing_sketch.sketch[i][j] - previous_smoothing.sketch[i][j])) + ((1-beta)*previous_trend.sketch[i][j])
    else:
        for i in range(0,depth):
            for j in range(0,width):
                trend_sketch.sketch[i][j] = observed_sketch.sketch[i][j] - previous_observed_sketch.sketch[i][j]

    #Forecasting sketch

    forecasting_sketch = KAry_Sketch(depth,width)
    for i in range(0,depth):
            for j in range(0,width):
                forecasting_sketch.sketch[i][j] = trend_sketch.sketch[i][j] + smoothing_sketch.sketch[i][j]

    return forecasting_sketch, smoothing_sketch, trend_sketch

def forecast(forecast_sketch,sketch_list,alpha):
    """Calls a Forecasting Model to build the forecast sketch from the list of sketches observed in the past

    Parameters
    ----------
    forecast_sketch : KAry_Sketch
        A forecast sketch
    sketch_list : list
        A list of observed sketches
    alpha : float
        The alpha value to be used by the EWMA

    Returns
    -------
    KAry_Sketch
        The forecast sketch
    """

    return EWMA(forecast_sketch,sketch_list[-2],alpha)

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
    cur_epoch = None #current epoch
    path = "traces/trace1.pcap" #path for the pcap file
    alpha = 0.7 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    T = 0.1 #threshold used by the change detection module
    w = 1 #number of past sketches saved for forecast ( =1 for EWMA)
    key_format = ["src","dst","dport","sport","proto"] #format of the key 
    keys = set()

    #-------------------------------------------- PROCESS INPUT --------------------------------------------#
    short_options = "hd:w:e:a:k:p:t:"                                                                                                                                         
    long_options = ["help", "depth=", "width=", "epoch=", "alpha=", "key=", "path=", "thresh="]
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
        if current_argument in ("-h", "--help"):
            print  ("------------------------------------------------------------------------------------\n",
                    "long argument   short argument  value               default                         \n",
                    "------------------------------------------------------------------------------------\n",
                    "--alpha          -a              positive float      0.7                            \n",
                    "--depth          -d              positive integer    5                              \n",
                    "--epoch          -e              positive float      0.1                            \n",
                    "--key            -k              \"opts...\"           \"src,dst,sport,dport,proto\"    \n",
                    "--path           -p              string              traces/trace1.pcap             \n",
                    "--thresh         -t              positive float      0.1                            \n",
                    "--width          -w              positive integer    5462                           \n",
                    "--------------------------------------------------------------------------------------")
            exit()
        elif current_argument in ("-d", "--depth"):
            print("Updating depth to", current_value)
            kary_depth = int(current_value)
        elif current_argument in ("-w", "--width"):
            print("Updating width to", current_value)
            kary_width = int(current_value)
        elif current_argument in ("-epoch", "--epoch"):
            print("Updating epoch to", current_value)
            kary_epoch = float(current_value)
        elif current_argument in ("-a", "--alpha"):
            print("Updating alpha to", current_value)
            alpha = float(current_value)
        elif current_argument in ("-k", "--key"):
            print("Updating key to", current_value)
            key = current_value.split(",")
        elif current_argument in ("-p", "--path"):
            print("Updating path to", current_value)
            path = current_value
        elif current_argument in ("-t", "--thresh"):
            print("Updating Threshold to", current_value)
            T = float(current_value)
                                                                                                        
    #----------------------------------------------- | | -----------------------------------------------#

    forecast_sketch = None
    error_sketch = None
    threshold = None

    trend_sketch = None #For use only with NSHW
    smoothing_sketch = None #For use only with NSHW
    
    #initialize sketch list
    sketch_list = [] #keeps current sketch [-1] and w past sketches
    for _ in range(0,w+1):
        sketch_list.append(KAry_Sketch(kary_depth,kary_width))

    packets = PcapReader(path)

    control = 1

    for packet in packets:
        #-------------------------------------------- EXTRACT PACKET FIELDS --------------------------------------------#
        src = packet.src
        dst = packet.dst
        try:
            sport = packet.sport
        except:
            sport = 0
        try:
            dport = packet.dport
        except:
            dport = 0
        try:
            proto = packet.proto
        except:
            proto = 0
        try:
            value = packet.len
        except:
            value = len(packet)

        key = []
        for elem in key_format:
            if elem == "src":
                key.append(src)
            if elem == "dst":
                key.append(dst)
            if elem == "sport":
                key.append(str(sport))
            if elem == "dport":
                key.append(str(dport))
            if elem == "proto":
                key.append(str(proto))

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
                forecast_sketch = forecast(forecast_sketch,sketch_list,alpha)

                #CHANGE DETECTION
                error_sketch, threshold = change(forecast_sketch,sketch_list[-1],T)
                print("Threshold =", threshold)
                #error_sketch.SHOW()
                for key in keys:
                    estimate = error_sketch.ESTIMATE(key)
                    if estimate  > threshold:
                        print("Change detected for:", key, "with estimate:", estimate, "at time:",cur_epoch)

            print("Changing epoch ")
            cur_epoch = packet["time"]

            if control == 1:
                control = 2

            #shift left, deleting first [0]
            for i in range(0,w):
                sketch_list[i] = copy.deepcopy(sketch_list[i+1])

            sketch_list[-1].RESET()
            keys.clear()

        #UPDATE SKETCH
        sketch_list[-1].UPDATE(packet["key"],packet["val"])

        #STORE KEY FOR CHANGE DETECTION
        keys.add(packet["key"])
    
if __name__ == "__main__":
  main()