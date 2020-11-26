from change import main_cycle
from scapy.all import rdpcap
import sys

def main():
    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    #kary_epoch = 5 #seconds per epoch
    alpha = 0.7 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    T = 0.5 #threshold used by the change detection module
    s = 2 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    key_format = ["src","dst","sport","dport","proto"] #format of the key, contains all possible options by default

    paths = ["traces/snmp-reflection-100k-2.pcap"]

    original_stdout = sys.stdout 
    #complex_results = []
    
    kary_epoch = 10

    Ts = [0.1,0.2,0.3,0.4,0.5,0.6,0.7]

    for path in paths:
      packets = rdpcap(path)
      for T in Ts:
        #TEST WITH MURMUR3
        #--------------------- TEST 1 ---------------------#
        
        key_format = ["src","dst","proto"]
        with open(path[7:-7] + '/' + path[7:-5] + "-" + str(kary_epoch) + '-' + forecasting_model + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
          sys.stdout = f
          _ , result = main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets)
          #complex_results.append(complex_result) 
          print(result)

        #--------------------- TEST 1 ---------------------#
        
        key_format = ["src","dst"]
        with open(path[7:-7] + '/' + path[7:-5] + "-" + str(kary_epoch) + '-' + forecasting_model + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
          sys.stdout = f
          _ , result = main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets)
          #complex_results.append(complex_result) 
          print(result)           
        
    sys.stdout = original_stdout


if __name__ == "__main__":
  main()