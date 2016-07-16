 #!/usr/bin/python

import curses, re
import printerTable

import texttable
from texttable import Texttable



class PrinterAP(printerTable.PrinterTable):
    
    CONSTANT = 191
    HEIGHT_TABLE = 25
    
    HEADER_AP_2 = ['ESSID'+" "*18,'BSSID'+" "*12, 'CH', 'AUT','DEAUT','ASS_RQ','ASS_RP','DIS','HAND_S','HAND_F','PWR','CORR','CORR%','DATA','RTS ','CTS ','ACK ','BEAC', 'PROBE_PQ', 'PROBE_RP', 'TOT_PACK']
    
    HEADER = [' ESSID'+" "*18,' BSSID'+" "*13, ' CH ', ' AUT ',' DEAUT ',' ASS_RQ ',' ASS_RP ',' DIS ',' HAND_S ',' HAND_F ',' PWR ',' CORR ',' CORR% ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC ', ' PROBE_PQ', ' PROBE_RP ', ' TOT_PACK']
    
    HEADER_AP_TMP = [' ESSID'+" "*18,' BSSID'+" "*13, 'CH ', ' AUT ',' DEAUT ',' ASS_RQ ',' ASS_RP ',' DIS ',' HAND_S ',' HAND_F ',' PWR ',' CORR ',' CORR% ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC ', ' PROBE_PQ', ' PROBE_RP ', ' TOT_PACK']
    
    
    def __init__(self, height):
        printerTable.PrinterTable.__init__(self, height)
        
        self.tableOrdAP = texttable.Texttable()
        self.tableOrdAP_2 = texttable.Texttable()
        self.tableSelected = texttable.Texttable()
        
        self.isSelected = False
        
        self.dimTableAP = 0
        self.dimTableAP_2 = 0

        self.indexHeaderFirst = 0
        self.indexHeaderAfter = 0

    
    def setIsSelected(self,isSelected):
        self.isSelected = isSelected
        
    def setIndexHeader(self, index):
        self.indexHeaderFirst = self.indexHeaderAfter
        self.indexHeaderAfter = index
        
    def drawTable(self):
        #self.clear()
        
        PrinterAP.HEADER[self.indexHeaderFirst] = PrinterAP.HEADER_AP_TMP[self.indexHeaderFirst]
        PrinterAP.HEADER[self.indexHeaderAfter] = re.sub("^ ", '>', PrinterAP.HEADER[self.indexHeaderAfter])
        
        self.src.addstr(0,0, str(PrinterAP.HEADER).strip("[]").replace("'","").replace(",",""), self.colorHeader)
        self.src.addstr(1,0, str("="*PrinterAP.CONSTANT))
        if self.indexCursor > 0:
            self.src.addstr(2, 0, self.tableOrdAP.draw())
            if self.isSelected:
                self.src.addstr(2+self.indexCursor, 0, self.tableSelected.draw(), curses.color_pair(4))
            else:
                self.src.addstr(2+self.indexCursor, 0, self.tableSelected.draw(), curses.color_pair(1))
            
            self.src.addstr(2+self.indexCursor+1, 0, " "*PrinterAP.CONSTANT)
            self.src.addstr(2+self.indexCursor+2, 0, self.tableOrdAP_2.draw())
            self.src.addstr(2+self.indexCursor + self.dimTableAP_2 +2, 0, " "*PrinterAP.CONSTANT)
        else:
            try:
                if self.isSelected:
                    self.src.addstr(2, 0, self.tableSelected.draw(), curses.color_pair(4))
                else:
                    self.src.addstr(2, 0, self.tableSelected.draw(), curses.color_pair(1))
                self.src.addstr(3, 0, " "*PrinterAP.CONSTANT)
                self.src.addstr(4, 0, self.tableOrdAP_2.draw())
                self.src.addstr(2+self.indexCursor + self.dimTableAP_2 +2, 0, " "*PrinterAP.CONSTANT)
            except:
                fifo = open("b.txt", "w+")
                fifo.write(self.tableSelected.draw())
                fifo.write("\n")
                fifo.close()
                



    def resetHeaderIndex(self, index):
        PrinterAP.HEADER[index] = PrinterAP.HEADER_AP_TMP[index]

    def refreshTable(self):
        self.src.refresh(self.mypad_pos_ap, 0, 30,0, 50,190)
    
    def reset(self):
        self.tableOrdAP.reset()
        self.tableOrdAP_2.reset()
        self.tableSelected.reset()
        
        self.dimTableAP = 0
        self.dimTableAP_2 = 0
    
    def cleanRow(self):
        if self.indexCursor < PrinterAP.HEIGHT_TABLE:
            start = self.dimTableAP + self.dimTableAP_2 + 1
            end = PrinterAP.HEIGHT_TABLE + start + 10
            for i in range(start, end):
                self.src.addstr(i, 0, " "*PrinterAP.CONSTANT)
    
    
    def init_table(self, table):
        table.set_deco(Texttable.HEADER)
        table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
    
    
    
    def createTable(self, indexAP):
        self.init_table(self.tableOrdAP)
        self.init_table(self.tableOrdAP_2)
        self.init_table(self.tableSelected)
        
        PrinterAP.HEADER[indexAP] = PrinterAP.HEADER_AP_TMP[indexAP]
        PrinterAP.HEADER[indexAP] = re.sub("^ ", '>', PrinterAP.HEADER[indexAP])
        
        self.tableOrdAP.add_rows([PrinterAP.HEADER_AP_2])
        self.tableOrdAP_2.add_rows([PrinterAP.HEADER_AP_2])
        self.tableSelected.add_rows([PrinterAP.HEADER_AP_2])
        
    
    
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
    
        
    def add_rows(self, tup, index):
        if index == 0:
            self.tableSelected.add_rows(tup, False)
        elif index == 1:
            self.tableOrdAP.add_rows(tup, False)
            self.dimTableAP += 1
        elif index == 2:
            self.tableOrdAP_2.add_rows(tup, False)
            self.dimTableAP_2 += 1


    def setMyPadPos(self, mypad_pos):
        self.mypad_pos_ap = mypad_pos
        
    def setIndexCursor(self, indexCursor):
        self.indexCursor = indexCursor



