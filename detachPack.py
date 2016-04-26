#!/usr/bin/python

import scapy
from scapy.all import *

import copy, sys
import os.path

class DetachPack:
    
    def __init__ (self, nameFile):
        self.packageList = []
        #self.name = "CAPT-"
        #self.extension = ".pcap"
        #self.contFile = 1
        
        #nameFile = self.name+str(self.contFile)+self.extension
        #existFile = os.path.exists(nameFile)
        ##if existFile:
        #while existFile:
            #self.contFile += 1
            #nameFile = self.name+str(self.contFile)+self.extension
            #existFile = os.path.exists(nameFile)
        
        self.pktdump = PcapWriter(nameFile, append=True, sync=True)
        
    def detach(self,p):
        
        self.pktdump.write(p)


