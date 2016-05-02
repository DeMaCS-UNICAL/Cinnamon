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
        
        
        #self.path = "path.fifo"
        #os.mkfifo(self.path)

        #fifo = open(path, "w")
        #fifo.write("Message from the sender!\n")
        #fifo.close()
        
        #self.pktdumpFifo = PcapWriter(self.path, append=True, sync=True)
        
    def detach(self,p):
        
        self.pktdump.write(p)
        
        #with gzip.open(self.path, 'wb') as f:
            #f.write(p)
        #self.pktdumpFifo.write(p)

    
    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
        
    def getStopSniff(self):
        return self.stopSniff

