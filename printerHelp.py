 #!/usr/bin/python

import curses, re
import printerF

import texttable
from texttable import Texttable


class PrinterHelp(printerF.Printer):
    
    HEIGHT_TABLE = 25
    
    def __init__(self, height):
        printerF.Printer.__init__(self, height) 
        

    def drawTable(self):
        self.src.addstr(0,0, "q = Exit\tTab = Change Selected Table\tr = Reverse Order Table\t\t> = Order Table Next Column\t< = Order Table Previous Column", curses.color_pair(1))
        #self.src.addstr(1,0, "> = Order Table Next Column\t< = Order Table Previous Column")
        
    def refreshTable(self):
        self.src.refresh(0, 0, 50,0, 50,190)
        
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
