from change import main_cycle
from scapy.all import rdpcap
import sys

def main():
    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    kary_epoch = 5 #seconds per epoch
    alpha = 0.7 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    T = 0.5 #threshold used by the change detection module
    s = 2 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    key_format = ["src","dst","sport","dport","proto"] #format of the key, contains all possible options by default

    #path = "traces/tcp-syn-reflection-100k-1.pcap" #path for the pcap file
    #path = "traces/tcp-syn-reflection-100k-2.pcap" #path for the pcap file
    #path = "traces/udp-flood-100k.pcap" #path for the pcap file
    #packets = rdpcap(path) #rdpcap is better when we are running multiple times
    original_stdout = sys.stdout 
    result = []

    #TEST WITH MURMUR3
    #--------------------- TEST 1 ---------------------#
    
    path = "traces/tcp-syn-reflection-100k-1.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.47
    kary_epoch = 5
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))               
    #--------------------- TEST 2 ---------------------#
    path = "traces/tcp-syn-reflection-100k-2.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.85
    kary_epoch = 5
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))           
    #--------------------- TEST 3 ---------------------#
    path = "traces/udp-flood-100k.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.25
    kary_epoch = 3
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))
    
    #TEST WITH CRC32
    hash_func = "crc32"
    #--------------------- TEST 1 ---------------------#
    path = "traces/tcp-syn-reflection-100k-1.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.47
    kary_epoch = 5
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))               
    #--------------------- TEST 2 ---------------------#
    path = "traces/tcp-syn-reflection-100k-2.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.85
    kary_epoch = 5
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))           
    #--------------------- TEST 3 ---------------------#
    path = "traces/udp-flood-100k.pcap"
    packets = rdpcap(path)
    key_format = ["dst","proto"]
    T = 0.25
    kary_epoch = 3
    with open(str(kary_epoch) + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      result.append(main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets))
    
    sys.stdout = original_stdout
if __name__ == "__main__":
  main()