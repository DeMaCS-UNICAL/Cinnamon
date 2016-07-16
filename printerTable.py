#!/usr/bin/python

import curses

class PrinterTable:
    
    HEIGHT_TABLE_CLIENT = 25
    
    def __init__(self, height):

        self.colorHeader = curses.A_BOLD
        self.colorHeader |= curses.color_pair(2)
        
        self.src = curses.newpad(height,300)
        self.src.nodelay(-1)
        
        self.height = height
        self.indexCursor = 0
        self.contInfoClient = 0
        self.pressedInfo = False
        
        self.mypad_pos_client = 0
        self.mypad_pos_ap = 0
        
        
        
    
    def setPressedInfo(self, pressedInfo):
        self.pressedInfo = pressedInfo
    
    
    def setContInfoClient(self, contInfoClient):
        self.contInfoClient = contInfoClient
        
    
    def getIndexCursor(self):
        return self.indexCursor
    
        
    def clear(self):
        #self.src.clrtobot()
        #self.src.clrtoeol()
        self.src.erase()
        #self.src.clear()
        #self.src.redrawwin()
        
        
