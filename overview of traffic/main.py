from pcap_parser import parse
import xlsxwriter
import sys
import statistics

class Window:
    def __init__(self,packets,size,keys):
        self.size = size
        self.time = []
        self.total = [0]
        self.values = []
        self.averages = []
        self.keys = keys

        for key in keys:
            self.values.append([0])

        self.time.append(float(packets[0]["time"]))
        for j in range(0,len(packets)):
            packet = packets[j]
            if packet["time"] > self.time[-1] + size:
                #Change Detection
                self.time.append(float(self.time[-1] + size))
                for list in self.values:
                    list.append(0)
                self.total.append(0)
                j = j - 1
                continue
            index = self.keys.index(str(packet["key"]))
            self.values[index][-1] = self.values[index][-1] + 1
            self.total[-1] = self.total[-1] + 1

        for row in self.values:
            self.averages.append([])
            for _value in row:
                self.averages[-1].append(0)

        for k in range(0,len(self.averages)):
            for t in range(0,len(self.averages[0])):
                val = [i for i in self.values[k][:t+1] if i != 0]
                if len(val) > 0:
                    self.averages[k][t] = statistics.mean(val)
                else:
                    self.averages[k][t] = 0

    def get_microbursts(self,factor,factor2,options=None):
        microbursts = []
        for k in range(1,len(self.averages)):
            for t in range(0,len(self.averages[0])):
                #Insert Criteria for Microburst:
                if self.values[k][t] > factor*self.averages[k][t] and self.values[k][t] > factor2*self.total[t]:
                    list = self.keys[k].split(' ')[-1].replace('\'','').replace('}','')
                    list1 = self.keys[k].split(' ')[-3].replace('\'','').replace('}','').replace(',','')
                    if list != 'None' and list1 != 'None':
                        print(str(list) + ' ' + str(list1) + ' ' + str(self.time[t]), end=' ')
                    #print("Microburst at time: " + str(self.time[t]) + " for the key: " + str(self.keys[k]) + " with value: " + str(self.values[k][t]) + " and a cumulative average of " + str(factor*self.averages[k][t]))
        print('')
        
    def get_F2(self):
        for t in range(0,len(self.values[0])):
            sum = 0
            for k in range(0,len(self.values)):
                sum = sum + (self.values[k][t]**2)
            print("Time: ", str(t), "      ", "F2: ", str(sum))
            

class Trace:
    def __init__(self,trace,epoch_sizes):
        self.windows = []
        self.sizes = []
        self.trace = trace
        self.cur_window = None
        self.packets = self.load_trace(trace)
        
        self.keys = []
        for packet in self.packets:
            if str(packet["key"]) not in self.keys:
                self.keys.append(str(packet["key"]))
                    
        for size in epoch_sizes:
            self.add_window(float(size))

    def load_trace(self,trace):
        try:
            output = parse(trace)
        except Exception as e:
            print(e)
        print("Finished Loading Trace")
        return output

    def add_window(self,size):
        self.sizes.append(size)
        self.windows.append(Window(self.packets,size,self.keys))
        if self.cur_window == None:
            self.cur_window = self.windows[0]

    def curr_window(self):
        print("Current Window:",self.cur_window.size)


def main():    
    path = sys.argv[1]
    epoch_sizes = sys.argv[2:]

    traces_names = []
    traces = []

    traces_names.append(path)
    traces.append(Trace(path,epoch_sizes))

    cur_trace = traces[-1]

    while(True):
        message = input("Action:\n")
        options = message.split(' ')
        action = options[0]
        args = options[1:]
        if action == "add":
            option = args[0]
            args = args[1:]
            if option == "window":
                try:
                    epoch_sizes = args
                    for window in epoch_sizes:
                        cur_trace.add_window(float(window))
                        print("Added the window",str(window),"to",str(cur_trace.trace))
                    pass
                except Exception as e:
                    print(e)
                finally:
                    continue
            elif option == "trace":
                try:
                    trace = args[0]
                    epoch_sizes = args[1:]

                    if trace not in traces_names:
                        print("Trace not in memory: Loading Trace...")
                        try:
                            if trace not in traces_names:
                                traces.append(Trace(trace,epoch_sizes))
                                traces_names.append(trace)
                                print("Added the trace",trace,"to the list.")
                        except:
                            print("Failed adding trace")
                            continue
                    else:
                        print("Trace already exists. Aborted.")
                except:
                    print("An error ocurred while adding trace")
                finally:
                    continue
        elif action == "select":
            option = args[0]
            args = args[1:]
            if option == "window":
                try:
                    window = float(args[0])
                    if window in cur_trace.sizes:
                        index = cur_trace.sizes.index(window)
                        cur_trace.cur_window = cur_trace.windows[index]
                    else:
                        print("This window size does not Exist!")

                finally:
                    continue
            elif option == "trace":
                try:
                    trace = args[0]
                    if trace in traces_names:
                        index = traces_names.index(trace)
                        cur_trace = traces[index]
                        cur_trace.cur_window = cur_trace.windows[0]
                    else:
                        print("This trace does not Exist!")

                finally:
                    continue
        elif action == "get":
            option = args[0]
            args = args[1:]
            if option == "microbursts":
                try:
                    print("Getting Microbursts")
                    factor = args[0]
                    factor2 = args[1]
                    cur_trace.cur_window.get_microbursts(float(factor),float(factor2))
                finally:
                    continue
            elif option == "f2":
                try:
                    print("Getting f2")
                    cur_trace.cur_window.get_F2()
                finally:
                    continue
            elif option == "status":
                print("Status:")
                print(cur_trace.trace)
                print(cur_trace.cur_window.size)
        elif action == "exit":
            exit()
        else:
            print("Option not supported!")


    #with xlsxwriter.Workbook('microbursts_' + str(output) + '.xlsx') as workbook:

    """         worksheet = workbook.add_worksheet("totals")
            worksheet.write_row(0,1,keys)
            worksheet.write_column(1,0,time)
            for i in range(0,len(keys)): 
                worksheet.write_column(1,i+1,values[i])

            worksheet = workbook.add_worksheet("averages")
            worksheet.write_row(0,1,keys)
            worksheet.write_column(1,0,time)
            for i in range(0,len(averages)): 
                worksheet.write_column(1,i+1,averages[i])

            worksheet = workbook.add_worksheet('Window Size ' + str(size_window))
            worksheet.write_column(0,0,time)
            worksheet.write_column(0,1,total)"""

if __name__ == "__main__":
  main()