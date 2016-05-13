#!/usr/bin/python

import printerInfo
import threading

import time
from time import sleep

class CheckPrinter (threading.Thread):

    def __init__(self, threadID, name, delay, printer):
        threading.Thread.__init__(self)
        
        self.printer = printer

        self.canPrint = False
        self.delay = delay
        
    
    def setCanPrint(self):
        #self.lock.acquire()
        self.canPrint = True
        #self.lock.release()
        
    def run(self):
        while not self.printer.getStopSniff():
            if self.canPrint:
                self.printer.printInformation()
                self.canPrint = False
                #sleep(self.delay)
            
