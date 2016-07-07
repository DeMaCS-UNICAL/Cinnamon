 #!/usr/bin/python

import curses, re
import curses.textpad

import printerF

import texttable
from texttable import Texttable


class PrinterHelp(printerF.Printer):
    
    HEIGHT_TABLE = 25
    
    def __init__(self, height):
        printerF.Printer.__init__(self, height) 
        

    def drawTable(self):
        #self.addTextBox()
        try:
            self.src.addstr(0,0, "q = Exit   Tab = Change Selected Table   r = Reverse Order Table   > = Order Table Next Column   < = Order Table Previous Column   + = Add Info    - = Remove Info", curses.color_pair(1))
        except Exception, e:
            self.fileLog = open("log.log", "a")
            self.fileLog.write(str(e))
            self.fileLog.close()
        ##self.src.addstr(1,0, "> = Order Table Next Column\t< = Order Table Previous Column")
        
    def refreshTable(self):
        self.src.refresh(0, 0, 50,0, 50,190)
        
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
        
    
    def addTextBox(self):
        self.src.addstr(0,0, "q = Exit   Tab = Change Selected Table   r = Reverse Order Table   > = Order Table Next Column   < = Order Table Previous Column   + = Add Info    - = Remove Info", curses.color_pair(1))
        
        win = curses.newwin(5, 60, 5, 5)
        win.border()
        global tb
        tb = curses.textpad.Textbox(win)
        
        text = tb.edit()
        self.src.addstr(0,0,text.encode('utf_8'))
        
