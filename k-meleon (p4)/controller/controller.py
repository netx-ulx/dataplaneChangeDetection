from kary_sketch import *
#from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import *
from crc import Crc
import socket, struct, pickle, os
import ipaddress 
import time
import itertools

crc32_polinomials = [0x04C11DB7, 0xEDB88320, 0xDB710641, 0x82608EDB, 0x741B8CD7, 0xEB31D82E,
                    0xD663B05, 0xBA0DC66B, 0x32583499, 0x992C1A4C, 0x32583499, 0x992C1A4C]

class CMSController(object):

    def __init__(self,width,port,set_hash):
        self.max_int = 4294967296
        self.controller = SimpleSwitchAPI(port)
        self.set_hash = set_hash
        self.custom_calcs = self.controller.get_custom_crc_calcs()
        self.register_num =  len(self.custom_calcs)
        self.width = width
        self.init()
        self.registers = []
        self.flag = None

    def init(self):
        if self.set_hash:
            self.set_crc_custom_hashes()
        self.create_hashes()

    def create_hashes(self):
        self.hashes = []
        for i in range(self.register_num):
            self.hashes.append(Crc(32, crc32_polinomials[i], True, 0xffffffff, True, 0xffffffff))

    def set_crc_custom_hashes(self):
        i = 0
        for custom_crc32, _width in sorted(self.custom_calcs.items()):
            self.controller.set_crc32_parameters(custom_crc32, crc32_polinomials[i], 0xffffffff, 0xffffffff, True, True)
            i+=1
       
    def decode_registers(self):
        self.read_registers()
        if self.registers[0] == None:
            return

        aux = []
        for value in self.registers[3]: #check values inside error_sketch
            if value > 4000000000:
                aux.append(value - self.max_int)
            else:
                aux.append(value)
        self.registers[3] = aux
    
    def read_registers(self):
        width = self.width
        self.registers = []
        self.registers.append(self.controller.register_read("reg_epoch_bit"))             #0 flag
        if self.registers[0] != self.flag:
            self.flag = self.registers[0]
            if (self.registers[0][0] == 0): #choose error and mv sketch
                mv_row0 = self.controller.register_read("reg_mv_sketch1_row0")
                mv_row1 = self.controller.register_read("reg_mv_sketch1_row1")
                mv_row2 = self.controller.register_read("reg_mv_sketch1_row2")
                err_row0 = self.controller.register_read("reg_error_sketch_row0")
                err_row1 = self.controller.register_read("reg_error_sketch_row1")
                err_row2 = self.controller.register_read("reg_error_sketch_row2")

                self.registers.append(mv_row0[width:2*width])             #1 src ips
                self.registers[1] = self.registers[1] + mv_row1[width:2*width]
                self.registers[1] = self.registers[1] + mv_row2[width:2*width]
                self.registers.append(mv_row0[2*width:3*width])           #2 dst ips
                self.registers[2] = self.registers[2] + mv_row1[2*width:3*width]
                self.registers[2] = self.registers[2] + mv_row2[2*width:3*width]
                self.registers.append(err_row0[width:2*width])          #3 error sketch
                self.registers[3] = self.registers[3] + err_row1[width:2*width]
                self.registers[3] = self.registers[3] + err_row2[width:2*width]
                self.registers.append(self.controller.register_read("reg_packet_changed"))  #4 total num packets

                #reset mv keys and counters
                self.controller.register_reset("reg_mv_sketch1_row0")
                self.controller.register_reset("reg_mv_sketch1_row1")
                self.controller.register_reset("reg_mv_sketch1_row2")
            else:
                mv_row0 = self.controller.register_read("reg_mv_sketch0_row0")
                mv_row1 = self.controller.register_read("reg_mv_sketch0_row1")
                mv_row2 = self.controller.register_read("reg_mv_sketch0_row2")
                err_row0 = self.controller.register_read("reg_error_sketch_row0")
                err_row1 = self.controller.register_read("reg_error_sketch_row1")
                err_row2 = self.controller.register_read("reg_error_sketch_row2")

                self.registers.append(mv_row0[width:2*width])      #1 src ips
                self.registers[1] = self.registers[1] + mv_row1[width:2*width]
                self.registers[1] = self.registers[1] + mv_row2[width:2*width]
                self.registers.append(mv_row0[2*width:3*width])      #2 dst ips
                self.registers[2] = self.registers[2] + mv_row1[2*width:3*width]
                self.registers[2] = self.registers[2] + mv_row2[2*width:3*width]
                self.registers.append(err_row0[0:width])      #2 dst ips
                self.registers[3] = self.registers[3] + err_row1[0:width]
                self.registers[3] = self.registers[3] + err_row2[0:width]
                self.registers.append(self.controller.register_read("reg_packet_changed"))  #4 total num packets

                print(self.registers[3])

                #reset mv keys and counters
                self.controller.register_reset("reg_mv_sketch0_row0")
                self.controller.register_reset("reg_mv_sketch0_row1")
                self.controller.register_reset("reg_mv_sketch0_row2")   
        else:
            self.registers[0] = None

    def flow_to_bytestream(self, flow):
        return socket.inet_aton(flow[0]) + socket.inet_aton(flow[1])

    def get_index(self, flow, width):
        values = []
        for i in range(self.register_num):
            index = self.hashes[i].bit_by_bit_fast((self.flow_to_bytestream(flow))) % width
            values.append(index)
        return values

    def detect_change(self,depth):
        splited = []
        width = len(self.registers[3])/depth
        for i in range(0,depth):
            splited.append(self.registers[3][i*width:((i+1)*width)])
        return splited, self.registers[1], self.registers[2], self.registers[4]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sw', help="switch name to configure" , type=str, required=False, default="s1")
    parser.add_argument('--port', help="thrift server port" , type=int, required=False, default="9090")
    parser.add_argument('--width', help="width of the sketch (number of buckets per row)", type=int, required=False, default=64)
    parser.add_argument('--thresh', help="threshold for the change detection module", type=float, required=False, default=0.5)
    parser.add_argument('--depth', help="depth of the sketch (number of rows)", type=int, required=False, default=3)
    parser.add_argument('--epoch', help="seconds in each epoch", type=int, required=False, default=1)
    args = parser.parse_args()

    controller = CMSController(args.width,args.port,True) #True if we want to use custom polynomials

    epoch = -1
    while(True):
        #retrieve data from data plane    
        controller.decode_registers()

        #check if a new epoch as been captured
        if controller.registers[0] == None:
            time.sleep(args.epoch)
            continue

        error, raw_src, raw_dst, num_packets = controller.detect_change(args.depth)
        error_sketch = KAry_Sketch(len(error),len(error[0]))
        error_sketch.sketch = error

        #do not perform change detection before the end of the second epoch
        if epoch <= 0:
            epoch = epoch + 1
            continue

        str_src = []
        for src in raw_src:
            if src > 0:
                binsrc = "{:032b}".format(src)
                str_src.append(str(int(binsrc[0:8],2))+"."+str(int(binsrc[8:16],2))+"."+str(int(binsrc[16:24],2))+"."+str(int(binsrc[24:32],2))) #get dst ip
            else:
                str_src.append("0")

        str_dst = []
        for dst in raw_dst:
            if dst > 0:
                bindst = "{:032b}".format(dst)
                str_dst.append(str(int(bindst[0:8],2))+"."+str(int(bindst[8:16],2))+"."+str(int(bindst[16:24],2))+"."+str(int(bindst[24:32],2))) #get dst ip
            else:
                str_dst.append("0")

        indexes = []
        for i in range(0,len(str_src)):
            if str_src[i] != "0":
                indexes.append(controller.get_index([str_src[i],str_dst[i]],args.width))
            else:
                indexes.append("0")

        k = []
        for i in range(0,len(str_dst)): 
            k.append([str_src[i],str_dst[i],indexes[i]])

        keys = []
        for key in k:
            if key in keys:
                pass
            else:
                keys.append(key)
        #error_sketch.SHOW()

        #Compute threshold
        TA = args.thresh * sqrt(error_sketch.ESTIMATEF2())

        #Estimate error for each key
        changes = []
        all_keys = []
        for i in range(0,len(keys)):
            if keys[i][0] != "0":
                estimate = error_sketch.ESTIMATE(keys[i][2])
                all_keys.append([(keys[i][0],keys[i][1],estimate,keys[i][2])])
                if estimate > TA:
                    changes.append((keys[i][0],keys[i][1],estimate,keys[i][2]))
                    #print("Change detected for:", keys[i][0] + "," + keys[i][1], "with estimate:", estimate)

        #write changes to file            
        with open("controller.out",'a') as f:
            f.write("Epoch: " + str(epoch) + "       " + "Threshold: " + str(TA) + "       " + "Num Packets: " + str(num_packets[0]) +'\n')
            f.write("Change: " + str(changes) + '\n')
            f.write("Number of Flows: " + str(len(all_keys)) + '\n')
        epoch = epoch + 1
        time.sleep(args.epoch)
