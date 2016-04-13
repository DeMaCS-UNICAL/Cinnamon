#!/usr/bin/python

import scapy
from scapy.all import *

import copy, sys
import os.path

class DetachPack:
    
    def __init__ (self):
        self.packageList = []
        self.name = "CAPT-"
        self.extension = ".pcap"
        self.contFile = 1
        
        nameFile = self.name+str(self.contFile)+self.extension
        existFile = os.path.exists(nameFile)
        #if existFile:
        while existFile:
            self.contFile += 1
            nameFile = self.name+str(self.contFile)+self.extension
            existFile = os.path.exists(nameFile)
        
        self.pktdump = PcapWriter(nameFile, append=True, sync=True)
        
    def detach(self,p):
        
       
        
        #pack = copy.copy(p)
        #self.packageList.append(pack)
        #p.show()
        self.pktdump.write(p)
        
        #wrpcap("FILE-01.pcap", p)
        #print "-------------------------------------"
        
        #subprocess.call("./monitoringAP.py -f Capture/tempPack.pcap", shell=True)
        
        #grep = subprocess.Popen(["grep", "-n", "^ba", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #grep.stdin.write(str(p))
        #grep.stdin.close()
        #grep.wait()
        #line in sys.stdin:
            #sys.stdout.write(line)
        
        
    #def takePackList(self):
        #return self.packageList
