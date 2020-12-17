from change import main_cycle
from scapy.all import rdpcap
import getopt, sys
from operator import itemgetter
from multiprocessing import Pool
from statistics import mean

def cycle(arguments):
    time = arguments[0]
    target = arguments[1]
    thresholds = arguments[2]
    keys = arguments[3]  
    kary_epoch = arguments[6]
    alpha = arguments[7]
    results = []
    for key_format in keys: 
        arguments[13] = key_format
        for threshold in thresholds: 
            arguments[9] = threshold
            false_positives = 0
            attack_found = False
            complex_result, _ = main_cycle(*arguments[4:])
            accuracies = []
            for epoch in complex_result:
                for change in epoch["res"]:
                    if target in change:
                        if float(epoch["epoch"][1]) <= time + 2*kary_epoch and float(epoch["epoch"][1]) >= time - kary_epoch:
                            attack_found = True
                            false_positives = false_positives - 1
                    false_positives = false_positives + 1
                accuracies.append((epoch["numKeys"] - len(epoch["res"]))/epoch["numKeys"])
            #print([false_positives/len(complex_result),mean(accuracies),false_positives,attack_found,[alpha,threshold,key_format]])
            sys.stdout.flush()
            if not attack_found:
                break
            results.append([false_positives/len(complex_result),mean(accuracies),false_positives,attack_found,[alpha,threshold,key_format]])
    return results

def main():
    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    kary_epoch = 20 #seconds per epoch
    alpha = 0.9 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    threshold = 0.2 #threshold used by the change detection module
    s = 1 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    key_format = ["dst","proto"] #format of the key, contains all possible options by default

    supported_hashes = ["murmur3","crc32"]
    supported_models = ["ma","ewma","nshw"]
    #-------------------------------------------- PROCESS INPUT --------------------------------------------#
    short_options = "a:d:e:f:h:k:s:t:w:"                                                                                                                                         
    long_options = ["help", "alpha=", "depth=", "epoch=", "fmodel=", "hash=", "key=", "saved=", "thresh=", "width="]
    # Get full command-line arguments but the first
    
    path = sys.argv[1]
    print("Testing", path)
    target = sys.argv[2]
    time = float(sys.argv[3])
    argument_list = sys.argv[4:]

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
        elif current_argument in ("-s", "--saved"):
            print("Updating number of past sketches saved to", current_value)
            s = int(current_value)
        elif current_argument in ("-t", "--thresh"):
            print("Updating Threshold to", current_value)
            threshold = float(current_value)
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

    packets = rdpcap(path)

    alphas = [0.6,0.7,0.8,0.9]
    thresholds = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6,0.7,0.8]
    keys = [["dst","proto"],["src","dst","proto"],["src","sport","dst","dport","proto"]]
    
    arguments = []
    for alpha in alphas:
        arguments.append([time,target,thresholds,keys,kary_depth,kary_width,kary_epoch,alpha,beta,threshold,s,hash_func,forecasting_model,key_format,packets])           
            
    pool = Pool(processes=4)
    results = pool.map(cycle, arguments)
    pool.close()
    
    final_results = []
    for result in results:
        for sub in result:
            final_results.append(sub)
    #---------------- CHOOSE BEST -----------------#
    sorted_results = sorted(final_results, key=itemgetter(0))
    best = None
    for result in sorted_results:
        if result[3] == True:
            if best == None:
                print("Best combination:",result[0],result[1],result[2],result[4])
                best = result[0]
                #print("Sorted Results:",sorted_results)
            elif result[0] == best:
                print("Other best combinations:",result[0],result[1],result[2],result[4])
            else:
                break

    sorted_results = sorted(final_results,reverse=True,key=itemgetter(1))
    best = None
    for result in sorted_results:
        if result[3] == True:
            if best == None:
                print("Best Accuracy combination:",result[0],result[1],result[2],result[4])
                best = result[0]
                #print("Sorted Results:",sorted_results)
            elif result[0] == best:
                print("Other Accuracy best combinations:",result[0],result[1],result[2],result[4])
            else:
                break
if __name__ == "__main__":
  main()