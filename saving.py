#!/usr/bin/python

import threading

import scapy
from scapy.all import *


class Saving (threading.Thread):
    
    def __init__(self, threadID, name, delay, detachPack, interface):
        threading.Thread.__init__(self)
        
        self.detachPack = detachPack
        self.stopSniff = False
        self.interface = interface
        
    def run(self):
        #while (not self.stopSniff):
        
        sniff(iface=self.interface, prn=self.detachPack.detach, stop_filter=self.isStopSniff)
            #self.stopSniff = True

    
    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
        
    def isStopSniff(self, p):
        if self.detachPack.getStopSniff():
            return True
        return False
