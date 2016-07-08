#!/usr/bin/python

import threading, curses, sys
import printerInfo
import updateDisplay
import checkPrinter
import curses.textpad

import time
from time import sleep

class Listener (threading.Thread):
    
    def __init__(self, threadID, name, delay, printer, checkPrint, update):
        threading.Thread.__init__(self)
        #super(Listener, self).__init__()
        #self._stop = threading.Event()
        self.setDaemon(True)
        
        self.printer = printer
        self.checkPrint = checkPrint
        self.update = update
        
        self.src = curses.newpad(50,300)
        self.src.keypad(True)
        
        self.src.nodelay(0)
        
        #self.close = False
        
        self.insertText = False


    #def stop(self):
        #self._stop.set()

    #def stopped(self):
        #return self._stop.isSet()
    
    #def setCloseTrue(self):
        #self.close = True
        ##cmd = ord('q')
        #self.src.nodelay(True)
    
    def run(self):
        cmd = ""
        while cmd != None:
            cmd = self.src.getch()
            
            #f = open("cmd.txt", "a")
            #f.write(str(cmd)+"\n")
            #f.close()
            if cmd == ord('q'):
                self.printer.setStopSniff(True)
                curses.endwin()
                cmd = None
                    ##break
                #elif cmd == ord('s'):
            elif cmd == curses.KEY_DOWN:
                self.printer.goDown()
                
            elif cmd == curses.KEY_UP:
                self.printer.goUp()
            elif cmd == ord("p"):
                if not self.printer.getPauseSniff():
                    self.printer.setPauseSniff(True)
                else:
                    self.printer.setPauseSniff(False)
            elif cmd == ord("+"):
                self.printer.plusInfo()
            elif cmd == ord("-"):
                self.printer.removeInfo()
            elif cmd == ord(">"):
                self.printer.nextColumnOrd()
            elif cmd == ord("<"):
                self.printer.previousColumnOrd()
            elif cmd == ord('\t'):
                self.printer.changeTable()
            elif cmd == ord("r"):
                self.printer.reverseOrderTable()
            elif cmd == ord("f"):
                self.insertText = True
                self.update.setCanPrint(False)
                
                sleep(0.1)
                
                inp = curses.newwin(7,50, 15,70)
                inp.border()
                curses.curs_set(1)
                
                inp.addstr(1,2, "Please enter a MAC-address:")
                input = inp.getstr(3, 2, 20)
                #inp.refresh()
                
                while not self.printer.macAddressPresent(input) and input != "":
                    try:
                        inp.clear()
                        inp.border()
                        
                        inp.addstr(1,2, "Please enter a MAC-address:")
                        inp.addstr(5,2, "MAC-address Wrong, try again")
                        #inp.refresh()
                        input = ""
                        inp.addstr(5,2, "")
                        input = inp.getstr(3, 2, 20)
                    except Exception, e:
                        self.fileLog = open("log.log", "a")
                        self.fileLog.write(str(e))
                        self.fileLog.close()
                
                
                self.printer.setChooseMacAddress(input)
                self.insertText = False
                self.update.setCanPrint(True)
                    
            elif cmd == 127:    #CODE FOR BACKSPACE
                curses.curs_set(0)
                self.printer.setChooseMacAddress("")
                self.insertText = False
                self.update.setCanPrint(True)
            
            if not self.insertText:
                self.update.setCanPrint(True)
                self.checkPrint.setCanPrint()
            
            #self.printer.printInformation()                


