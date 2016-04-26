#!/usr/bin/python

import curses

class Printer:
    
    HEIGHT_TABLE_CLIENT = 25
    
    def __init__(self, height):
        
        self.colorHeader = curses.A_BOLD
        self.colorHeader |= curses.color_pair(2)
        
        self.height = height
        self.src = curses.newpad(height,300)
    
        self.indexCursor = 0
        self.contInfoClient = 0
        self.pressedInfo = False
    
        self.src.nodelay(1)
        self.src.keypad(True)
        
        self.mypad_pos_client = 0
        self.mypad_pos_ap = 0
        
        #self.listener()
        
    
    def setPressedInfo(self, pressedInfo):
        self.pressedInfo = pressedInfo
    
    
    #def setIndexCursor(self, indexCursor, whatDo):
        #if whatDo == 0:
            #self.indexCursor = indexCursor
        #elif whatDo == 1:
            #self.indexCursor += indexCursor
        #elif whatDo == 2:
            #self.indexCursor -= indexCursor
        
    
    def setContInfoClient(self, contInfoClient, whatDo):
        if whatDo == 0:
            self.contInfoClient = contInfoClient
        elif whatDo == 1:
            self.contInfoClient += contInfoClient
        elif whatDo == 2:
            self.contInfoClient -= contInfoClient
        
    
    def getIndexCursor(self):
        return self.indexCursor
    
        
    def clear(self):
        self.src.clear()
        
        
