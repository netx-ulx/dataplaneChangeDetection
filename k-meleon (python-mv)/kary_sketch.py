import string
from statistics import median
from math import sqrt
import getopt, sys
import binascii

from crc import Crc
import socket, struct, pickle, os
import ipaddress 
import time

crc32_polinomials = [0x04C11DB7, 0xEDB88320, 0xDB710641, 0x82608EDB, 0x741B8CD7, 0xEB31D82E,
                    0xD663B05, 0xBA0DC66B, 0x32583499, 0x992C1A4C, 0x32583499, 0x992C1A4C]

class KAry_Sketch:
    """
    A class used to represent a K-ary Sketch structure

    Attributes
    ----------
    depth : int 
        The depth of the sketch: number of rows
    width : int
        The width of the sketch: number of buckets in each row

    Methods
    -------
    UPDATE(key,value)
        Updates the sketch with the value for a given key
    ESTIMATE(key)
        Estimates the value for a given key
    sum()
        Calculates the sum of all values in the sketch
    ESTIMATEF2()
        Calculates the estimated second moment (F2) of the sketch
    SHOW()
        Prints the sketch matrix
    RESET()
        Resets the sketch by zeroing the sketch matrix
    """

    def __init__(self,depth,width):
        """
        Parameters
        ----------
        depth : int 
            The depth of the sketch: number of rows
        width : int
            The width of the sketch: number of buckets in each row
        """
        
        self.depth = depth
        self.width = width
        self.sketch = []
        self.keys = []
        self.counts = []
        self.seeds = []
        #initialize the sketch structure
        for i in range(0,depth):
            self.sketch.append([])
            for _ in range(0,width):
                self.sketch[i].append(0)

        for i in range(0,depth):
            self.keys.append([])
            for _ in range(0,width):
                self.keys[i].append((None,None))

        for i in range(0,depth):
            self.counts.append([])
            for _ in range(0,width):
               self.counts[i].append(0)
        #initialize the hash seeds for each row
        #for i in range(0,depth):
            #self.seeds.append(mmh3.hash64("K-ARY SKETCH",i)[0])

        self.init()

    def init(self):
        self.create_hashes()

    def UPDATE(self,key,value,hash_func):
        """Updates the sketch with the value for a given key

        Parameters
        ----------
        key : tuple 
            A five-tuple key (src,dst,sport,dport,proto)
        value : float 
            The value to be updated
        hash_func : string 
            The hash function to be used
        """
        #Update values
        for i in range(0,self.depth):
            bucket = None
            if hash_func == "crc32":
                bucket = self.get_index(key)[i]
            #Update K-ary
            self.sketch[i][bucket] = self.sketch[i][bucket] + value

            #if key not in self.keys:
                #self.keys.append(key)

            #Update MV
            if self.keys[i][bucket][0] == key[0] and self.keys[i][bucket][1] == key[1]:
                self.counts[i][bucket] = self.counts[i][bucket] + 1
            else:
                self.counts[i][bucket] = self.counts[i][bucket] - 1
                if self.counts[i][bucket] < 0:
                    self.keys[i][bucket] = key
                    self.counts[i][bucket] = - self.counts[i][bucket]

    def ESTIMATE(self,key,hash_func):
        """Estimates the value for a given key

        Parameters
        ----------
        key : tuple 
            A five-tuple key (src,dst,sport,dport,proto)
        hash_func : string 
            The hash function to be used
        
        Returns
        -------
        float
            The estimated value for a given key
        """

        result = []
        for i in range(0,self.depth):
            bucket = None
            if hash_func == "crc32":
                bucket = self.get_index(key)[i]
            #elif hash_func == "murmur3":
                #bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            result.append((self.sketch[i][bucket] - (self.sum(i)/self.width)) / (1 - (1/self.width)))
        return median(result)

    def get_index(self, flow):
        values = []
        for i in range(self.depth):
            index = self.hashes[i].bit_by_bit_fast((self.flow_to_bytestream(flow))) % self.width
            values.append(index)
        return values

    def flow_to_bytestream(self, flow):
        return socket.inet_aton(flow[0]) + socket.inet_aton(flow[1])

    def create_hashes(self):
        self.hashes = []
        for i in range(self.depth):
            self.hashes.append(Crc(32, crc32_polinomials[i], True, 0xffffffff, True, 0xffffffff))

    def QUERY(self,key,hash_func):
        """Estimates the value for a given key

        Parameters
        ----------
        key : tuple 
            A five-tuple key (src,dst,sport,dport,proto)
        hash_func : string 
            The hash function to be used
        
        Returns
        -------
        float
            The estimated value for a given key
        """

        result = []
        buckets = []
        for i in range(0,self.depth):
            bucket = None
            if hash_func == "crc32":
                bucket = self.get_index(key)[i]
            #elif hash_func == "murmur3":
                #bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            buckets.append(bucket)
            result.append(self.sketch[i][bucket])
        return result,buckets

    def sum(self,i):
        """Calculates the sum of all values in the sketch
        
        Returns
        -------
        float
            The sum of all values in the sketch
        """
        return sum(self.sketch[i])

    def ESTIMATEF2(self):
        """Calculates the estimated second moment (F2) of the sketch
        
        Returns
        -------
        float
            The estimated F2 of the sketch
        """

        result = []
        for i in range(0,self.depth):
            aux = 0
            for j in range(0,self.width):
                aux = aux + (self.sketch[i][j]**2)
            result.append(((self.width/(self.width-1))*aux) - ((1/(self.width-1))*(self.sum(i)**2)))
        return median(result)

    def COMBINE(self,sketch):
        #TODO
        pass

    def SHOW(self):
        """Prints the sketch matrix"""

        print(self.sketch)

    def RESET(self):
        """Resets the sketch by zeroing the sketch matrix"""
        #self.keys = []
        for i in range(0,self.depth):
            for j in range(0,self.width):
                self.sketch[i][j] = 0
                self.keys[i][j] = (None,None)
                self.counts[i][j] = 0
