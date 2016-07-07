#!/usr/bin/python

import threading, curses, sys
import printerInfo
import checkPrinter


class Listener (threading.Thread):
    
    def __init__(self, threadID, name, delay, printer, checkPrint):
        threading.Thread.__init__(self)
        #super(Listener, self).__init__()
        #self._stop = threading.Event()
        self.setDaemon(True)
        
        self.printer = printer
        self.checkPrint = checkPrint
        self.src = curses.newpad(50,300)
        self.src.keypad(True)
        
        self.src.nodelay(0)
        
        self.close = False


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
            if cmd == ord('q') or self.close:
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
            self.checkPrint.setCanPrint()
            
            #self.printer.printInformation()                
            
            
            
