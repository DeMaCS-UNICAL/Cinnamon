#!/usr/bin/python

import analyzePackage
import printerInfo
import checkPrinter

import threading

import time
from time import sleep

class UpdateDisplay (threading.Thread):
    
    def __init__(self, threadID, name, delay, printer, analyzePack, checkPrint):
        threading.Thread.__init__(self)
        
        self.delay = delay
        
        self.printer = printer
        self.analyzePack = analyzePack
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
                self.info = self.analyzePack.takeInformation()
                self.infoAP = self.analyzePack.takeInformationAP()
                self.infoClient = self.analyzePack.takeInformationClient()
                
                self.printer.addInfo(self.info)
                self.printer.addInfoAP(self.infoAP)
                self.printer.addInfoClient(self.infoClient)
                
                self.checkPrint.setCanPrint()
                
                #self.printer.printInformation()
                #self.checkPrint.setCanPrint()
                #self.checkPrint.setBooleanAndPrint()
                sleep(self.delay)
        
        self.stopSniff = True

