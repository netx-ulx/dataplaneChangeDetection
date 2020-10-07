from scapy.all import rdpcap, copy, PcapReader
import mmh3
import string
from statistics import median
from math import sqrt
import getopt, sys
import binascii

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
        self.seeds = []
        #initialize the sketch structure
        for i in range(0,depth):
            self.sketch.append([])
            for _ in range(0,width):
                self.sketch[i].append(0)
        #initialize the hash seeds for each row
        for i in range(0,depth):
            self.seeds.append(mmh3.hash64("K-ARY SKETCH",i)[0])

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

        for i in range(0,self.depth):
            bucket = None
            if hash_func == "crc32":
                bucket = binascii.crc32(str.encode(','.join(key)),self.seeds[i])%self.width
            elif hash_func == "murmur3":
                bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            self.sketch[i][bucket] = self.sketch[i][bucket] + value

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
                bucket = binascii.crc32(str.encode(','.join(key)),self.seeds[i])%self.width
            elif hash_func == "murmur3":
                bucket = mmh3.hash64(','.join(key),self.seeds[i])[0]%self.width
            result.append( (self.sketch[i][bucket] - (self.sum()/self.width)) / (1 - (1/self.width)))
        return median(result)

    def sum(self):
        """Calculates the sum of all values in the sketch
        
        Returns
        -------
        float
            The sum of all values in the sketch
        """

        return sum(self.sketch[0])

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
            result.append(((self.width/(self.width-1))*aux) - ((1/(self.width-1))*(self.sum()**2)))
        return median(result)

    def COMBINE(self,sketch):
        #TODO
        pass

    def SHOW(self):
        """Prints the sketch matrix"""

        print(self.sketch)

    def RESET(self):
        """Resets the sketch by zeroing the sketch matrix"""

        for i in range(0,self.depth):
            for j in range(0,self.width):
                self.sketch[i][j] = 0
