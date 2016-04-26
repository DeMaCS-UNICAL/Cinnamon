 #!/usr/bin/python

import curses, re
import printerF

import texttable
from texttable import Texttable



class PrinterClient(printerF.Printer):
    
    HEIGHT_TABLE = 25
    
    HEADER = [' STATION             ', ' AUTH',' DEAUTH ', ' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR%',' DATA  ',' RTS ',' CTS ',' ACK',' BEACON  ', ' PROBE_REQ  ', ' TOT_PACK']
    
    HEADER_CLIENT_2 = ['STATION            ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR%','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK']
    
    HEADER_CLIENT_TMP = [' STATION             ', ' AUTH',' DEAUTH ', ' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR%',' DATA  ',' RTS ',' CTS ',' ACK',' BEACON  ', ' PROBE_REQ  ', ' TOT_PACK']
    
   
    HEADER_INFO_2 = ['ESSID                 ','BSSID              ','STATION            ','AUTH  ','DEAUTH  ','PWR  ','HAND_SUCC  ','HAND_FAIL  ','CORRUPT  ','CORR%  ','DATA   ','RTS  ','CTS  ','ACK  ','BEACON  ', 'PROBE_REQ  ', 'TOT_PACK']
    
    
    def __init__(self, height):
        printerF.Printer.__init__(self, height) 
        
        self.tableInfo = texttable.Texttable()
        self.tableOrdClient = texttable.Texttable()
        self.tableOrdClient_2 = texttable.Texttable()
        self.tableOrdClientSelect = texttable.Texttable()
        
        
    def drawTable(self):
        self.src.insstr(0,0, str(PrinterClient.HEADER).strip("[]").replace("'","").replace(",",""), curses.color_pair(2))
        self.src.insstr(1,0, str("="*141))
        #if not self.tupl:
            #self.src.insstr(2, 0, self.tableOrdClient.draw())
        #else:
        if self.indexCursor > 0:
            self.src.insstr(2, 0, self.tableOrdClient.draw())
            self.src.insstr(2+self.indexCursor, 0, self.tableOrdClientSelect.draw(), curses.color_pair(1))
            if not self.pressedInfo:
                self.src.insstr(2+self.indexCursor+2, 0, self.tableOrdClient_2.draw())
            else:
                self.src.insstr(2+self.indexCursor+2, 0, str(PrinterClient.HEADER_INFO_2).strip("[]").replace("'","").replace(",","") , curses.color_pair(3))
                self.src.insstr(2+self.indexCursor+3,0, str("="*183))
                self.src.insstr(4+self.indexCursor+2, 0, self.tableInfo.draw())
                self.src.insstr(7+self.contInfoClient+self.indexCursor, 0, self.tableOrdClient_2.draw())
        else:
            if not self.pressedInfo:
                self.src.insstr(2, 0, self.tableOrdClientSelect.draw(), curses.color_pair(1))
                self.src.insstr(4, 0, self.tableOrdClient_2.draw())
            else:
                self.src.insstr(2, 0, self.tableOrdClientSelect.draw(), curses.color_pair(1))
                self.src.insstr(2+self.indexCursor+2, 0, str(PrinterClient.HEADER_INFO_2).strip("[]").replace("'","").replace(",","") , curses.color_pair(3))
                self.src.insstr(2+self.indexCursor+3,0, str("="*183))
                self.src.insstr(4+self.indexCursor+2, 0, self.tableInfo.draw())
                self.src.insstr(7+self.contInfoClient+self.indexCursor, 0, self.tableOrdClient_2.draw())
                        
    
    def resetHeaderIndex(self, index):
        PrinterClient.HEADER[index] = PrinterClient.HEADER_CLIENT_TMP[index]
                        
    
    def refreshTable(self):
        self.src.refresh(self.mypad_pos_client, 0, 0, 0, PrinterClient.HEIGHT_TABLE, 190)
        
    
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
    
        
    def reset(self):
        self.tableInfo.reset()
        self.tableOrdClient.reset()
        self.tableOrdClient_2.reset()
        self.tableOrdClientSelect.reset()
    
    
    def createTable(self, header, indexClient):
        
        #self.tableInfo.reset()
        #self.tableOrdClient.reset()
        #self.tableOrdClient_2.reset()
        #self.tableOrdClientSelect.reset()
        
        self.tableInfo.set_deco(Texttable.HEADER)
        self.tableInfo.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableInfo.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableInfo.add_rows([[header[0], header[1], header[2], header[3], header[4], header[5], header[6], header[7], header[8], header[9], header[10], header[11], header[12], header[13], header[14], header[15], header[16]]])
        
        
        self.init_table(self.tableOrdClient)
        self.init_table(self.tableOrdClient_2)
        self.init_table(self.tableOrdClientSelect)
        
        #self.tableOrdClient.set_deco(Texttable.HEADER)
        #self.tableOrdClient.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        #self.tableOrdClient.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.tableOrdClient_2.set_deco(Texttable.HEADER)
        #self.tableOrdClient_2.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        #self.tableOrdClient_2.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.tableOrdClientSelect.set_deco(Texttable.HEADER)
        #self.tableOrdClientSelect.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        #self.tableOrdClientSelect.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
        
        
        PrinterClient.HEADER[indexClient] = PrinterClient.HEADER_CLIENT_TMP[indexClient]
        #header_client[indexClient] = re.sub("^", ' ', header_client[indexClient])
        PrinterClient.HEADER[indexClient] = re.sub("^ ", '>', PrinterClient.HEADER[indexClient])
        #header_client[indexClient] = header_client[indexClient] + ">"
        
        self.tableOrdClient.add_rows([PrinterClient.HEADER_CLIENT_2])
        self.tableOrdClient_2.add_rows([PrinterClient.HEADER_CLIENT_2])
        self.tableOrdClientSelect.add_rows([PrinterClient.HEADER_CLIENT_2])
    
    
    
    def init_table(self, table):
        table.set_deco(Texttable.HEADER)
        table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
    
    
    def add_rows(self, tup, index):
        if index == 0:
            self.tableOrdClientSelect.add_rows(tup, False)
        elif index == 1:
            self.tableOrdClient.add_rows(tup,False)
        elif index == 2:
            self.tableOrdClient_2.add_rows(tup,False)
        elif index == 3:
            self.tableInfo.add_rows(tup,False)
        
    
    def setMyPadPos(self, mypad_pos):
        self.mypad_pos_client = mypad_pos



    def setIndexCursor(self, indexCursor, whatDo):
        if whatDo == 0:
            self.indexCursor = indexCursor
        elif whatDo == 1:
            self.indexCursor += indexCursor
        elif whatDo == 2:
            self.indexCursor -= indexCursor
