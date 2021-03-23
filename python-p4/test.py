from change import main_cycle
from pcap_parser import parse
import getopt, sys
from operator import itemgetter
from multiprocessing import Pool
from statistics import mean

def cycle(arguments):
    targets = arguments[0]
    thresholds = arguments[1] 
    kary_epoch = arguments[4]
    alpha = arguments[5]
    beta = arguments[6]
    key_format = arguments[11]
    results = []
    #TEST ALL THRESHOLDS
    for threshold in thresholds: 
        arguments[7] = threshold
        false_positives = 0
        attacks_found = 0
        #EXECUTE SOLUTION WITH THE PARAMETERS SELECTED
        complex_result, _ = main_cycle(*arguments[2:])
        accuracies = []
        cycle_targets = targets.copy() #used to compare know attacks vs attacks found
        #Check if any known attack was found in any of the epochs
        for epoch in complex_result:
            for change in epoch["res"]:
                for target in targets:
                    if target[0] in change:
                        if float(epoch["epoch"][1]) <= float(target[1]) + kary_epoch and float(epoch["epoch"][1]) >= float(target[1]) - kary_epoch: #If known attack is present in the changes for its epoch
                            if target in targets:
                                if target in cycle_targets:
                                    attacks_found = attacks_found + 1
                                    cycle_targets.remove(target)
                                false_positives = false_positives - 1
                false_positives = false_positives + 1
            accuracies.append((epoch["numKeys"] - len(epoch["res"]))/epoch["numKeys"])
        sys.stdout.flush()
        #If the attack was not found for a given threshold, skip same configuration for bigger thresholds
        if attacks_found == 0:
            break
        precision = attacks_found / (attacks_found + false_positives)
        recall = attacks_found / (attacks_found + (len(targets) - attacks_found))
        if arguments[10] == "nshw":
            #print([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,attacks_found,[alpha,beta,threshold,key_format]])
            results.append([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,attacks_found,[alpha,beta,threshold,key_format]])
        else:
            #print([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,attacks_found,[alpha,threshold,key_format]])
            results.append([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,attacks_found,[alpha,threshold,key_format]])
    return results

def main():
    #------------------------------------------ DEFAULT PARAMETERS ------------------------------------------#

    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    kary_epoch = 20 #seconds per epoch
    beta = 0.7 #beta to be used by the NSHW
    s = 1 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    supported_hashes = ["murmur3","crc32"]
    supported_models = ["ewma","nshw"]

    #-------------------------------------------- PROCESS INPUT --------------------------------------------#

    short_options = "d:e:f:h:s:w:"                                                                                                                                         
    long_options = ["help", "depth=", "epoch=", "fmodel=", "hash=", "saved=", "width="]
    # Get full command-line arguments but the first
    
    path = sys.argv[1]
    print("Testing", path)

    #Get known attacks and timestamps from argv
    targets = []
    i = 2
    while i < len(sys.argv):
        if not sys.argv[i].startswith("-"):
            targets.append([sys.argv[i],sys.argv[i+1]])
            i = i + 2
        else:
            break

    #Get configuration options from argv
    argument_list = sys.argv[i:]
    try:
        arguments, _ = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)

    # Evaluate given options
    for current_argument, current_value in arguments:
        if current_argument in ("-d", "--depth"):
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
        elif current_argument in ("-s", "--saved"):
            print("Updating number of past sketches saved to", current_value)
            s = int(current_value)
        elif current_argument in ("-w", "--width"):
            print("Updating width to", current_value)
            kary_width = int(current_value)
        elif current_argument in ("--help"):
            print  ("------------------------------------------------------------------------------------\n",
                    "long argument   short argument  value               default                         \n",
                    "------------------------------------------------------------------------------------\n",
                    "--depth          -d              positive integer    5                              \n",
                    "--epoch          -e              positive float      0.1                            \n",
                    "--fmodel         -f              string              ewma                           \n",
                    "--hash           -h              string              murmur3                        \n",
                    "--saved          -s              positive integer    1                              \n",
                    "--width          -w              positive integer    5462                           \n",
                    "--------------------------------------------------------------------------------------")
            sys.exit(2)
                                                                                                        
    #------------------------------------------------------ | | ------------------------------------------------------#

    packets = parse(path)
    print("Finished parsing packets")

    #--------------------------------------------- PARAMETERS FOR TESTING --------------------------------------------#

    alphas = [0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    betas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    thresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    keys = [["dst","proto"],["src","dst","proto"],["src","sport","dst","dport","proto"]]

    
    #------------------------------------ PREPARING ARGUMENTS FOR PARALLELIZATION ------------------------------------#
    
    arguments = []
    if forecasting_model == "nshw":
        for key_format in keys:
            for alpha in alphas:
                for beta in betas:
                    arguments.append([targets,thresholds,kary_depth,kary_width,kary_epoch,alpha,beta,None,s,hash_func,forecasting_model,key_format,packets])           
    else:
        for key_format in keys:
            for alpha in alphas:
                arguments.append([targets,thresholds,kary_depth,kary_width,kary_epoch,alpha,beta,None,s,hash_func,forecasting_model,key_format,packets]) 
    #---------------------------------------------- PARALLEL EXECUTION  ----------------------------------------------#

    pool = Pool(processes=6)
    results = pool.map(cycle, arguments)
    pool.close()
    
    #----------------------------------------------- ORGANIZE RESULTS ------------------------------------------------#

    final_results = []
    for result in results:
        for sub in result:
            final_results.append(sub)
    
    #------------------------------------------- CHOOSE BEST CONFIGURATION -------------------------------------------#

    sorted_results = sorted(final_results, key=itemgetter(0))
    best = None
    for result in sorted_results:
        if result[3] > 0:
            if best == None:
                print("Best combination:",result[0],result[1],result[2],result[3],result[4],result[5],result[6])
                best = result[0]
                #print("Sorted Results:",sorted_results)
            elif result[0] == best:
                print("Other best combinations:",result[0],result[1],result[2],result[3],result[4],result[5],result[6])
            else:
                break

    sorted_results = sorted(final_results,reverse=True,key=itemgetter(1))
    best = None
    for result in sorted_results:
        if result[3] > 0:
            if best == None:
                print("Best Accuracy combination:",result[0],result[1],result[2],result[3],result[4],result[5],result[6])
                best = result[0]
                #print("Sorted Results:",sorted_results)
            elif result[0] == best:
                print("Other Accuracy best combinations:",result[0],result[1],result[2],result[3],result[4],result[5],result[6])
            else:
                break

if __name__ == "__main__":
  main()