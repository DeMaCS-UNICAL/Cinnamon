#!/usr/bin/python

import scapy
from scapy.all import *

import copy, sys
import os.path
import os
import gzip


class DetachPack:

    #def __init__(self):
        #self.stopSniff = False
    
    def __init__ (self, nameFile):
        self.stopSniff = False
        self.pktdump = PcapWriter(nameFile, append=True, sync=True)
        
        
        #self.path = "path"
        #os.mkfifo(self.path)

        #self.fifo = open(self.path, "w+")
        #with open(self.fifo, mode='w', buffering=-1) as fb:
        #self.pktdumpFifo = PcapWriter("path", append=True, sync=False)
        #fifo.write("Message from the sender!\n")
        #fifo.close()
        
        
    def detach(self,p):
        
        self.pktdump.write(p)
        
        #with gzip.open(self.path, 'wb') as f:
            #f.write(p)
        #self.pktdumpFifo.write(p)
        #self.fifo.write(p)
    
    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
        
    def getStopSniff(self):
        return self.stopSniff

