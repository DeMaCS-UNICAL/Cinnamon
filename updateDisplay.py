#!/usr/bin/python

import interfaceScript
import printerInfo
import checkPrinter

import threading

import time
from time import sleep

class UpdateDisplay (threading.Thread):
    
    def __init__(self, threadID, name, delay, printer, sniffer, checkPrint):
        threading.Thread.__init__(self)
        
        self.delay = delay
        
        self.printer = printer
        self.sniffer = sniffer
        self.checkPrint = checkPrint
        
        self.canPrint = False
        self.stopSniff = False
        
        self.info = {}
        self.infoAP = {}
        self.infoClient = {}
        
    
    def getStopSniff(self):
        return self.stopSniff
    
    def run(self):
        while not self.printer.getStopSniff():
            
            if not self.printer.getPauseSniff():
            #if self.canPrint:
                self.info = self.sniffer.takeInformation()
                self.infoAP = self.sniffer.takeInformationAP()
                self.infoClient = self.sniffer.takeInformationClient()
                
                self.printer.addInfo(self.info)
                self.printer.addInfoAP(self.infoAP)
                self.printer.addInfoClient(self.infoClient)
                
                self.checkPrint.setCanPrint()
                
                #self.printer.printInformation()
                #self.checkPrint.setCanPrint()
                #self.checkPrint.setBooleanAndPrint()
                sleep(self.delay)
        
        self.stopSniff = True

