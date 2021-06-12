from change import main_cycle
from pcap_parser import parse
import getopt, sys

def main():
    kary_depth = 5 #number of rows
    kary_width = 5462 #number of buckets in each row
    kary_epoch = 1000 #packets per epoch
    alpha = 0.6 #alpha to be used by the EWMA and NSHW
    beta = 0.7 #beta to be used by the NSHW
    T = 0.5 #threshold used by the change detection module
    s = 1 #number of past sketches saved for forecast (=1 for EWMA)
    hash_func = "murmur3" #hashing algorithm to be used by the sketch module
    forecasting_model = "ewma" #forecasting model to be used by the forecasting module
    key_format = ["src","dst","dport","sport","proto"] #format of the key, contains all possible options by default

    supported_hashes = ["murmur3","crc32"]
    supported_models = ["ma","ewma","nshw"]

    #-------------------------------------------- PROCESS INPUT --------------------------------------------#
    short_options = "a:d:e:f:h:k:s:t:w:"                                                                                                                                         
    long_options = ["help", "alpha=", "depth=", "epoch=", "fmodel=", "hash=", "key=", "saved=", "thresh=", "width="]
    # Get full command-line arguments but the first
    
    path = sys.argv[1]
    argument_list = sys.argv[2:]

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
            kary_epoch = int(current_value)
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

    original_stdout = sys.stdout 

    packets = parse(path)
    print("Finished parsing packets")

    complex_result, _ = main_cycle(kary_depth,kary_width,kary_epoch,alpha,beta,T,s,hash_func,forecasting_model,key_format,packets)
    total_num_packets = 0
    with open('output/' + str(kary_depth) + '-' + path[10:-5] + "-" + str(kary_epoch) + '-' + forecasting_model + '-' + hash_func + '-' + '-'.join(key_format) + '-' + str(T) + '.out', 'w') as f:
      sys.stdout = f
      for epoch in complex_result:
        print("Epoch:", epoch["epoch"][1][1], "      " + "Threshold: " + str(epoch["epoch"][0]), "      " + "Num Packets: " + str(epoch["epoch"][3]))
        print(epoch["res"])
        total_num_packets = total_num_packets + int(epoch["epoch"][4])
        print("Num Keys:",str(epoch["epoch"][4]))
        #print(epoch["moment"])

    sys.stdout = original_stdout
    print("Total Num Keys:",total_num_packets)
if __name__ == "__main__":
  main()