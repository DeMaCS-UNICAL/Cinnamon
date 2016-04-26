 #!/usr/bin/python

import curses, re
import printerF

import texttable
from texttable import Texttable



class PrinterAP(printerF.Printer):
    
    HEADER = [' ESSID               ',' BSSID             ',' AUTH ',' DEAUTH ',' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR% ',' DATA ',' RTS ',' CTS ',' ACK ',' BEACON ', ' PROBE_REQ ', ' TOT_PACK']
    
    HEADER_AP_2 = ['ESSID               ','BSSID            ','AUTH','DEAUTH','PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR%','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK']
    
    HEADER_AP_TMP = [' ESSID               ',' BSSID             ',' AUTH ',' DEAUTH ',' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR% ',' DATA ',' RTS ',' CTS ',' ACK ',' BEACON ', ' PROBE_REQ ', ' TOT_PACK']
    
    
    def __init__(self, height):
        printerF.Printer.__init__(self, height)
        
        self.tableOrdAP = texttable.Texttable()
        self.tableOrdAP_2 = texttable.Texttable()
        self.tableSelected = texttable.Texttable()
        
        
    def drawTable(self):
        self.src.insstr(0,0, str(PrinterAP.HEADER).strip("[]").replace("'","").replace(",",""), curses.color_pair(2))
        self.src.insstr(1,0, str("="*162))
        
        if self.indexCursor > 0:
            self.src.insstr(2, 0, self.tableOrdAP.draw())
            self.src.insstr(2+self.indexCursor, 0, self.tableSelected.draw(), curses.color_pair(1))
            
            self.src.insstr(2+self.indexCursor+2, 0, self.tableOrdAP_2.draw())
        else:
            self.src.insstr(2, 0, self.tableSelected.draw(), curses.color_pair(1))
            self.src.insstr(4, 0, self.tableOrdAP_2.draw())



    def resetHeaderIndex(self, index):
        PrinterAP.HEADER[index] = PrinterAP.HEADER_AP_TMP[index]

    def refreshTable(self):
        self.src.refresh(0,0, 29,0, 50,190)
    
    def reset(self):
        self.tableOrdAP.reset()
        self.tableOrdAP_2.reset()
        self.tableSelected.reset()
        
        
    
    def createTable(self, indexAP):
        #self.tableOrdAP.reset()
        #self.tableOrdAP_2.reset()
        #self.tableSelected.reset()
        
        self.tableOrdAP.set_deco(Texttable.HEADER)
        self.tableOrdAP.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableOrdAP.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableOrdAP_2.set_deco(Texttable.HEADER)
        self.tableOrdAP_2.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableOrdAP_2.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableSelected.set_deco(Texttable.HEADER)
        self.tableSelected.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableSelected.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])

        PrinterAP.HEADER[indexAP] = PrinterAP.HEADER_AP_TMP[indexAP]
        PrinterAP.HEADER[indexAP] = re.sub("^ ", '>', PrinterAP.HEADER[indexAP])
        #header_ap[indexAP] = re.sub("^ ", '>', header_ap[indexAP])
        #header_ap[indexAP] = header_ap[indexAP] + ">"
        
        self.tableOrdAP.add_rows([PrinterAP.HEADER_AP_2])
        self.tableOrdAP_2.add_rows([PrinterAP.HEADER_AP_2])
        self.tableSelected.add_rows([PrinterAP.HEADER_AP_2])
        
        
        
    def add_rows(self, tup, index):
        if index == 0:
            self.tableSelected.add_rows(tup, False)
        elif index == 1:
            self.tableOrdAP.add_rows(tup, False)
        elif index == 2:
            self.tableOrdAP_2.add_rows(tup, False)


    def setMyPadPos(self, mypad_pos):
        self.mypad_pos_ap = mypad_pos
        
    def setIndexCursor(self, indexCursor, whatDo):
        if whatDo == 0:
            self.indexCursor = indexCursor
        elif whatDo == 1:
            self.indexCursor += indexCursor
        elif whatDo == 2:
            self.indexCursor -= indexCursor
