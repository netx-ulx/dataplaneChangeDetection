from kary_sketch import *
from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import *
from crc import Crc
import socket, struct, pickle, os
import ipaddress 
import time

crc32_polinomials = [0x04C11DB7, 0xEDB88320, 0xDB710641, 0x82608EDB, 0x741B8CD7, 0xEB31D82E,
                    0xD663B05, 0xBA0DC66B, 0x32583499, 0x992C1A4C, 0x32583499, 0x992C1A4C]

#crc32_polinomials = [0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7,
#                     0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7, 0x04C11DB7]

class CMSController(object):

    def __init__(self,port,set_hash):
        self.max_int = 4294967295
        self.controller = SimpleSwitchAPI(port)
        self.set_hash = set_hash
        self.custom_calcs = self.controller.get_custom_crc_calcs()
        self.register_num =  len(self.custom_calcs)

        self.init()
        self.registers = []

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

        """In the decoding function you were free to compute whatever you wanted.
           This solution includes a very basic statistic, with the number of flows inside the confidence bound.
        """
        self.read_registers()
        new_registers = []
        for register in self.registers:
            aux = []
            for value in register:
                if value > 4000000000:
                    aux.append(value - self.max_int)
                else:
                    aux.append(value)
            new_registers.append(aux)
        self.registers = new_registers
    
    def read_registers(self):
        self.registers = []
        self.registers.append(self.controller.register_read("sketch_flag"))         #0 
        self.registers.append(self.controller.register_read("sketch_key0"))         #1 src and dst ips
        self.registers.append(self.controller.register_read("sketch_key1"))         #2 sport, dport and proto
        if (self.registers[0][0] == 0): #choose error sketch
            self.registers.append(self.controller.register_read("error_sketch1"))   #3 error sketch
        else:
            self.registers.append(self.controller.register_read("error_sketch0"))   #3 error sketch


    def detect_change(self,depth):
        splited = []
        epoch = len(self.registers[3])/depth
        for i in range(0,depth):
            splited.append(self.registers[3][i*epoch:((i+1)*epoch)-1])
        return splited, [self.registers[1],self.registers[2]]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sw', help="switch name to configure" , type=str, required=False, default="s1")
    parser.add_argument('--port', help="thrift server port" , type=int, required=False, default="9090")
    parser.add_argument('--width', help="width of the sketch (number of buckets per row)", type=int, required=False, default=32)
    parser.add_argument('--depth', help="depth of the sketch (number of rows)", type=int, required=False, default=3)
    parser.add_argument('--epoch', help="seconds in each epoch", type=int, required=False, default=20)
    parser.add_argument('--option', help="controller option can be either set_hashes, decode or reset registers", type=str, required=False, default="set_hashes")
    args = parser.parse_args()

    set_hashes = args.option == "set_hashes"
    controller = CMSController(args.port,True) #True if we want to use custom polynomials

    if args.option == "detect":
        while(True):    
            controller.decode_registers()
            error, raw_keys = controller.detect_change(args.depth)
            error_sketch = KAry_Sketch(len(error),len(error[0]))
            error_sketch.sketch = error
            print(". Sketch Flag: " + str(controller.registers[0][0]))
            print(". Error Sketch:")
            error_sketch.SHOW()
            print(".")

            str_keys0 = []
            for key in raw_keys[0]:
                if key > 0:
                    strkey = []
                    numKey = []
                    binkey = "{0:64b}".format(key).replace(" ","0")
                    strkey.append(str(int(binkey[32:40],2))+"."+str(int(binkey[40:48],2))+"."+str(int(binkey[48:56],2))+"."+str(int(binkey[56:64],2)-1)) #get src ip
                    strkey.append(str(int(binkey[0:8],2))+"."+str(int(binkey[8:16],2))+"."+str(int(binkey[16:24],2))+"."+str(int(binkey[24:32],2)+1)) #get dst ip

                    str_keys0.append(strkey)
                else:
                    str_keys0.append(["None"])

            str_keys1 = []
            for key in raw_keys[1]:
                if key > 0:
                    binkey = "{0:b}".format(key)
                    strkey = []
                    strkey.append(str(int(binkey[-16:],2)-1)) #get the src port
                    strkey.append(str(int(binkey[-32:-16],2))) #get the dst port
                    strkey.append(str(int(binkey[-40:-32],2)+1)) #get protocol

                    str_keys1.append(strkey)
                else:
                    str_keys1.append(["None"])

            keys = []
            for i in range(0,len(raw_keys[0])):
                keys.append(str_keys0[i] + str_keys1[i])
                print("Key " + str(i) + ": " + str(str_keys0[i] + str_keys1[i]))

            print(".")
            print(".^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.^.")
            print(".")

            time.sleep(args.epoch)