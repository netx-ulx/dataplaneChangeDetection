from kary_sketch import *
from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import *
from crc import Crc
import socket, struct, pickle, os
import ipaddress 
import time

class CMSController(object):

    def __init__(self,port):
        self.max_int = 4294967295
        self.controller = SimpleSwitchAPI(port)
        self.registers = []
       
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
        self.registers.append(self.controller.register_read("error_sketch0"))
        self.registers.append(self.controller.register_read("error_sketch1"))
        self.registers.append(self.controller.register_read("control_flag"))
        self.registers.append(self.controller.register_read("extra_op_counter"))
        self.registers.append(self.controller.register_read("sketch_flag")) 
        self.registers.append(self.controller.register_read("sketch_key0")) #src and dst ips
        self.registers.append(self.controller.register_read("sketch_key1")) #sport, dport and proto
        print(".")
        print(self.registers[3])
        print(".")

    def detect_change(self):
        n=3
        if (self.registers[4][0] == 0):
            splited = []
            epoch = len(self.registers[1])/n
            for i in range(0,n):
                splited.append(self.registers[1][i*epoch:((i+1)*epoch)-1])
            return splited, [self.registers[5],self.registers[6]]
        else:
            splited = []
            epoch = len(self.registers[1])/n
            for i in range(0,n):
                splited.append(self.registers[0][i*epoch:((i+1)*epoch)-1])
            return splited, [self.registers[5],self.registers[6]]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sw', help="switch name to configure" , type=str, required=False, default="s1")
    parser.add_argument('--port', help="thrift server port" , type=int, required=False, default="9090")
    parser.add_argument('--option', help="controller option can be either set_hashes, decode or reset registers", type=str, required=False, default="set_hashes")
    args = parser.parse_args()

    set_hashes = args.option == "set_hashes"
    controller = CMSController(args.port)

    if args.option == "detect":
        while(True):    
            controller.decode_registers()
            error, raw_keys = controller.detect_change()
            error_sketch = KAry_Sketch(len(error),len(error[0]))
            error_sketch.sketch = error
            print(". Sketch Flag: " + str(controller.registers[4][0]))
            print(". Error Sketch:")
            error_sketch.SHOW()
            print(".")

            str_keys0 = []
            for key in raw_keys[0]:
                if key > 0:
                    strkey = []
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

            time.sleep(20)