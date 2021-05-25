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

    def ESTIMATE(self,buckets):
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
            bucket = buckets[i]
            result.append((float(self.sketch[i][bucket]) - (float(self.sum(i))/float(self.width))) / (1.0 - (1.0/float(self.width))))
        return median(result)

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
            aux = 0.0
            for j in range(0,self.width):
                aux = aux + (self.sketch[i][j]**2) 
	    result.append(((float(self.width)/(float(self.width)-1.0))*float(aux)) - ((1.0/(float(self.width)-1.0))*(self.sum(i)**2.0)))
        return median(result)

    def COMBINE(self,sketch):
        #TODO
        pass

    def SHOW(self):
        """Prints the sketch matrix"""

        for row in self.sketch:
            print(str(row) + " Sum: " + str(sum(row)) + "; AbsSum: " + str(sum(abs(number) for number in row)))

    def RESET(self):
        """Resets the sketch by zeroing the sketch matrix"""

        for i in range(0,self.depth):
            for j in range(0,self.width):
                self.sketch[i][j] = 0
