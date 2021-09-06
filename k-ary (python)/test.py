from change import main_cycle
from pcap_parser import parse
import getopt, sys
from operator import itemgetter
from multiprocessing import Pool
from statistics import mean
import sys

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
        speed = []
        arguments[7] = threshold
        false_positives = 0
        attacks_found = 0
        true_positives = 0
        num_keys = 0
        outoftime = 0
        #EXECUTE SOLUTION WITH THE PARAMETERS SELECTED
        complex_result, _ = main_cycle(*arguments[2:])
        accuracies = []
        cycle_targets = targets.copy() #used to compare know attacks vs attacks found
        #Check if any known attack was found in any of the epochs
        for epoch in complex_result:
            num_keys = num_keys + epoch["numKeys"]
            for change in epoch["res"]:
                found = 0
                for target in targets:
                    if float(epoch["epoch"][1][1]) - 5*kary_epoch <= float(target[1]) and float(epoch["epoch"][1][1]) + kary_epoch >= float(target[1]): #If known attack is present in the changes for its epoch   
                        if target[0] in change:
                            found = 1
                            break
                if found == 1:
                    continue
                else:
                    false_positives = false_positives + 1
            for target in targets:
                if float(epoch["epoch"][1][1]) - kary_epoch <= float(target[1]) and float(epoch["epoch"][1][1]) + kary_epoch >= float(target[1]): #If known attack is present in the changes for its epoch   
                    for change in epoch["res"]:
                        if target[0] in change:
                            #if speed == 0 or float(epoch["epoch"][1][1]) + kary_epoch - float(target[1]) < speed:
                            speed.append("{:.3f}".format(float(epoch["epoch"][1][1]) + kary_epoch - float(target[1])))
                            true_positives = true_positives + 1
            to_remove = []
            for target in cycle_targets:
                if float(epoch["epoch"][1][1]) - kary_epoch <= float(target[1]) and float(epoch["epoch"][1][1]) + kary_epoch >= float(target[1]): #If known attack is present in the changes for its epoch   
                    for change in epoch["res"]:
                        if target[0] in change:
                            attacks_found = attacks_found + 1
                            to_remove.append(target)
                            break
            for item  in to_remove:
                cycle_targets.remove(item)
            accuracies.append((epoch["numKeys"] - len(epoch["res"]))/epoch["numKeys"])
        sys.stdout.flush()
        #If the attack was not found for a given threshold, skip same configuration for bigger thresholds
        #if true_positives == 0:
            #break
        
        false_negatives = len(cycle_targets)
        true_negatives = num_keys - (false_negatives+false_positives+true_positives)
        
        accuracy = (true_positives + true_negatives) / num_keys

        if true_positives == 0 and false_positives == 0:
            precision = 0
        else:
            precision = true_positives / (true_positives + false_positives)

        recall = true_positives/(true_positives+false_negatives)
        
        if arguments[10] == "nshw":
            print([round(false_positives/len(complex_result),3),round(mean(accuracies),3),round(precision,3),round(recall,3),false_positives,true_positives,false_negatives,attacks_found,[alpha,beta,threshold,key_format],speed])
            results.append([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,true_positives,[alpha,beta,threshold,key_format]])
        else:
            print(["{:.3f}".format(accuracy),"{:.3f}".format(precision),"{:.3f}".format(recall),false_positives,true_positives,false_negatives,true_negatives,[kary_epoch,alpha,threshold,key_format],attacks_found,speed])
            #print([false_positives/len(complex_result),mean(accuracies),precision,recall,false_positives,true_positives,attacks_found,len(cycle_targets),[kary_epoch,alpha,threshold,key_format],speed])
            results.append([accuracy,precision,recall,false_positives,true_positives,[kary_epoch,alpha,threshold,key_format],speed])
    return results

def main():
    #------------------------------------------ DEFAULT PARAMETERS ------------------------------------------#

    kary_depth = 3 #number of rows
    kary_width = 64 #number of buckets in each row
    kary_epoch = 20 #seconds per epoch
    beta = 0.7 #beta to be used by the NSHW
    s = 1 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "crc32" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    supported_hashes = ["murmur3","crc32"]
    supported_models = ["ewma","nshw"]

    #-------------------------------------------- PROCESS INPUT --------------------------------------------#

    short_options = "d:e:f:h:s:w:"                                                                                                                                         
    long_options = ["help", "depth=", "epoch=", "fmodel=", "hash=", "saved=", "width="]
    # Get full command-line arguments but the first
    
    path = sys.argv[1]
    print("Testing", path)
    sys.stdout.flush()
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
    sys.stdout.flush()
    #--------------------------------------------- PARAMETERS FOR TESTING --------------------------------------------#

    alphas = [0.5,0.625]

    epochs = [0.1,1,10,60,120,240]
    thresholds = [0.45,0.6,0.8]
    keys = [["src","dst"]]

    
    #------------------------------------ PREPARING ARGUMENTS FOR PARALLELIZATION ------------------------------------#
    print("Targets: " + str(len(targets)))
    sys.stdout.flush()
    arguments = []
    if forecasting_model == "ewma":
        for key_format in keys:
            for alpha in alphas:
                for kary_epoch in epochs:
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