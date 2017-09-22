 #!/usr/bin/python

import curses, re
import curses.textpad

import printerTable

import texttable
from texttable import Texttable


class PrinterHelp(printerTable.PrinterTable):
    
    HEIGHT_TABLE = 25
    
    def __init__(self, height):
        printerTable.PrinterTable.__init__(self, height) 
        

    def drawTable(self):
        #self.addTextBox()
        try:
            self.src.addstr(0,0, "q = Exit   p = Pause   f = Search   Tab = Change Selected Table   r = Reverse Order Table   > = Order Table Next Column   < = Order Table Previous Column   + = Add Info   - = Remove Info", curses.color_pair(1))
        except Exception, e:
            self.fileLog = open("log.log", "a")
            self.fileLog.write(str(e))
            self.fileLog.close()
        ##self.src.addstr(1,0, "> = Order Table Next Column\t< = Order Table Previous Column")
        
    def refreshTable(self):
        self.src.refresh(0, 0, 45,0, 45,190)
        
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
        
