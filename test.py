from change import main_cycle
from scapy.all import rdpcap

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


    packets = rdpcap(path) #rdpcap is better when we are running multiple times
    main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets)
    
if __name__ == "__main__":
  main()