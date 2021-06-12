from pcap_parser import parse
import xlsxwriter
import sys
import statistics

def main():    
    path = sys.argv[1]
    ip1 = sys.argv[2]
    #beginning = int(sys.argv[3])
    #end = int(sys.argv[4])
    size_windows = sys.argv[3:]


    packets = parse(path)
    print("Finished parsing packets")
        
    for size_window in size_windows:
        with xlsxwriter.Workbook('speeds_' + str(path[10:]) + '_' + str(size_window) + '.xlsx') as workbook:
            print("Size Window: " + str(size_window))

            total = [0]
            one = [0]
            two = [0]
            speeds = [0]
            time = []
            time.append(float(packets[0]["time"]))
            j = 0
            while j < len(packets):
                packet = packets[j]
                if packet["time"] > time[-1] + float(size_window):
                    #Change Detection
                    
                    speeds[-1] = total[-1] / float(size_window) 
                    speeds.append(0)
                    total.append(0)
                    one.append(0)
                    two.append(0)
                    time.append(float(time[-1] + float(size_window)))
                else:
                    if packet["key"]["src"] == ip1:
                        one[-1] = one[-1] + 1
                    elif packet["key"]["dst"] == ip1:
                        two[-1] = two[-1] + 1
                    total[-1] = total[-1] + 1
                    j = j + 1
            
            print("length of total: " + str(len(total)))
            print("sum of total: " + str(sum(total)))
            print("length of speeds: " + str(len(speeds)))
            
            #worksheet = workbook.add_worksheet()
            #worksheet.write_column(0,0,time)
            #worksheet.write_column(0,1,total)
            #worksheet.write_column(0,2,one)
            #worksheet.write_column(0,3,two)


if __name__ == "__main__":
  main()