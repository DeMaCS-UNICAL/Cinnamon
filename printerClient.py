 #!/usr/bin/python

import curses, re
import printerF

import texttable
from texttable import Texttable



class PrinterClient(printerF.Printer):
    
    HEIGHT_TABLE = 27
    CONSTANT = 187
    
    
    HEADER = [' STATION'+" "*14, ' CH', ' AUT',' DEAUT ', ' ASS_RQ ',' ASS_RP ',' DISASS ',' HAND_S ',' HAND_F ',' CORR  ',' CORR%  ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC  ', ' PROBE_RQ  ', ' PROBE_RP  ', ' TOT_PACK', ' OTHER', ' CONT']
    
    HEADER_CLIENT_2 = ['STATION'+" "*14, 'CH', 'AUT','DEAUT','ASS_RQ','ASS_RP','DISASS','HAND_S','HAND_F','CORR','CORR%','DATA','RTS ','CTS ','ACK ','BEAC', 'PROBE_RQ  ', 'PROBE_RP', 'TOT_PACK', 'OTHER','CONT']
    
    HEADER_CLIENT_TMP = [' STATION'+" "*14, ' CH', ' AUT', ' DEAUT ',' ASS_RQ ',' ASS_RP ',' DISASS ',' HAND_S ',' HAND_F ',' CORR  ',' CORR%  ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC  ', ' PROBE_RQ  ', ' PROBE_RP  ', ' TOT_PACK', ' OTHER', ' CONT']
    
   
    HEADER_INFO_2 = ['ESSID'+" "*17,'BSSID'+" "*14,'AUT  ','DEAUT ', 'ASS_RQ ',' ASS_RP  ',' DISASS  ','HAND_S  ','HAND_F  ','PWR ','CORR  ','CORR%   ','DATA ','RTS   ','CTS   ','ACK   ','BEAC  ', 'PROBE_RQ  ', 'PROBE_RP ', 'TOT_PACK']
    
    
    def __init__(self, height):
        printerF.Printer.__init__(self, height) 
        
        self.tableInfo = texttable.Texttable()
        self.tableOrdClient = texttable.Texttable()
        self.tableOrdClient_2 = texttable.Texttable()
        self.tableOrdClientSelect = texttable.Texttable()
        
        self.dimTableInfo = 0
        self.dimTableClient = 0
        self.dimTableClient_2 = 0
        self.selected = 0
        
        self.isSelected = False
        
        self.indexHeaderFirst = 0
        self.indexHeaderAfter = 0
        
        
    
    def setIndexHeader(self, index):
        self.indexHeaderFirst = self.indexHeaderAfter
        self.indexHeaderAfter = index
    
    def setIsSelected(self,isSelected):
        self.isSelected = isSelected
    
    def drawTable(self):
        PrinterClient.HEADER[20] = "CONT = "
        PrinterClient.HEADER[20] += str(self.dimTableClient+self.dimTableClient_2+self.selected)
        self.clear()

        PrinterClient.HEADER[self.indexHeaderFirst] = PrinterClient.HEADER_CLIENT_TMP[self.indexHeaderFirst]
        PrinterClient.HEADER[self.indexHeaderAfter] = re.sub("^ ", '>', PrinterClient.HEADER[self.indexHeaderAfter])
        
        self.src.addstr(0,0, str(PrinterClient.HEADER).strip("[]").replace("'","").replace(",",""), self.colorHeader)
        self.src.addstr(1,0, str("="*187))
        if self.indexCursor > 0:
            try:
                self.src.addstr(2, 0, self.tableOrdClient.draw())
                if self.isSelected:
                    self.src.addstr(2+self.indexCursor, 0, self.tableOrdClientSelect.draw(), curses.color_pair(4))
                else:
                    self.src.addstr(2+self.indexCursor, 0, self.tableOrdClientSelect.draw(), curses.color_pair(1))
                if not self.pressedInfo:
                    self.src.addstr(2+self.indexCursor+1, 0, str(" "*PrinterClient.CONSTANT))
                    self.src.addstr(2+self.indexCursor+2, 0, self.tableOrdClient_2.draw())
                else:
                    #self.tableInfo.draw().decode('utf-8')
                    self.src.addstr(2+self.indexCursor+1,0, str(" "*PrinterClient.CONSTANT))
                    self.src.addstr(2+self.indexCursor+2,0, str("-"*PrinterClient.CONSTANT))
                    self.src.addstr(2+self.indexCursor+3, 0, str(PrinterClient.HEADER_INFO_2).strip("[]").replace("'","").replace(",","") , curses.color_pair(3))
                    self.src.addstr(2+self.indexCursor+4,0, str("="*PrinterClient.CONSTANT))
                    self.src.addstr(4+self.indexCursor+3, 0, self.tableInfo.draw())
                #if self.contInfoClient < 2:
                    #self.src.addstr(7+self.contInfoClient+self.indexCursor, 0, str(" "*PrinterClient.CONSTANT))
                    self.src.addstr(7+self.indexCursor+self.contInfoClient,0, str("-"*PrinterClient.CONSTANT))
                    self.src.addstr(10+self.contInfoClient+self.indexCursor, 0, self.tableOrdClient_2.draw())
                    #self.src.addstr(8+self.contInfoClient+self.indexCursor, 0, str(" "*PrinterClient.CONSTANT))
                #self.src.addstr(8+self.contInfoClient+self.indexCursor+1, 0, str(" "*PrinterClient.CONSTANT))
                    #self.tableInfo.draw().decode('utf-8')
            except Exception, e:
                self.fileLog = open("log.log", "w+")
                self.fileLog.write(str(e))
                self.fileLog.close()
                    
        else:
            try:
                if self.isSelected:
                    self.src.addstr(2+self.indexCursor, 0, self.tableOrdClientSelect.draw(), curses.color_pair(4))
                else:
                    self.src.addstr(2, 0, self.tableOrdClientSelect.draw(), curses.color_pair(1))
                if not self.pressedInfo:
                    self.src.addstr(3, 0, " "*PrinterClient.CONSTANT)
                    self.src.addstr(4, 0, self.tableOrdClient_2.draw())
                else:
                    #try:
                    #self.tableInfo.draw().decode('utf-8')
                    self.src.addstr(2+self.indexCursor+1,0, " "*PrinterClient.CONSTANT)
                    self.src.addstr(2+self.indexCursor+2,0, "-"*PrinterClient.CONSTANT)
                    self.src.addstr(2+self.indexCursor+3, 0, str(PrinterClient.HEADER_INFO_2).strip("[]").replace("'","").replace(",","") , curses.color_pair(3))
                    self.src.addstr(2+self.indexCursor+4,0, "="*PrinterClient.CONSTANT)
                    self.src.addstr(4+self.indexCursor+3, 0, self.tableInfo.draw())
                    #self.src.addstr(6+self.contInfoClient+self.indexCursor, 0, " "*PrinterClient.CONSTANT)
                    #if self.contInfoClient < 2:
                        #self.src.addstr(6+self.contInfoClient+self.indexCursor, 0, str(" "*PrinterClient.CONSTANT))
                    self.src.addstr(7+self.indexCursor+self.contInfoClient, 0, str("-"*PrinterClient.CONSTANT))
                    self.src.addstr(10+self.contInfoClient+self.indexCursor, 0, self.tableOrdClient_2.draw())
                    #self.src.addstr(8+self.contInfoClient+self.indexCursor, 0, str(" "*PrinterClient.CONSTANT))
                #except Exception, e:
                    #self.fileLog = open("log.log", "a")
                    #self.fileLog.write(str(e)+"\n")
                    #self.fileLog.close()
                    #self.tableInfo.draw().decode('utf-8')
                #self.src.addstr(7+self.contInfoClient+self.indexCursor,0, " "*PrinterClient.CONSTANT)
            except Exception, e:
                self.fileLog = open("log.log", "a")
                self.fileLog.write(str(e))
                self.fileLog.close()
                        
    
    def cleanRow(self):
        try:
            if self.indexCursor < PrinterClient.HEIGHT_TABLE:
                start = self.dimTableClient + self.dimTableClient_2 + 1
                end = PrinterClient.HEIGHT_TABLE + start + 10
                for i in range(start, end):
                    self.src.addstr(i, 0, " "*PrinterClient.CONSTANT)
        except Exception, e:
            self.fileLog = open("log.log", "a")
            self.fileLog.write(str(e))
            self.fileLog.close()
    
    def resetHeaderIndex(self, index):
        PrinterClient.HEADER[index] = PrinterClient.HEADER_CLIENT_TMP[index]

    
    def refreshTable(self):
        try:
            LINES, COL = self.src.getmaxyx()
        
            self.src.refresh(self.mypad_pos_client, 0, 0, 0, PrinterClient.HEIGHT_TABLE, 190)
        except Exception, e:
            self.fileLog = open("log.log", "a")
            self.fileLog.write(str(e))
            self.fileLog.close()
            
    
    def resizeTable(self, height):
        self.height = height
        self.src.resize(height, 300)
    
        
    def reset(self):
        self.tableInfo.reset()
        self.tableOrdClient.reset()
        self.tableOrdClient_2.reset()
        self.tableOrdClientSelect.reset()
        
        self.dimTableClient = 0
        self.dimTableClient_2 = 0
        self.dimTableInfo = 0
    
    
    def createTable(self, header, indexClient):
        
        self.tableInfo.set_deco(Texttable.HEADER)
        self.tableInfo.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableInfo.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableInfo.add_rows([[header[0], header[1], header[2], header[3], header[4], header[5], header[6], header[7], header[8], header[9], header[10], header[11], header[12], header[13], header[14], header[15], header[16], header[17], header[18], header[19]]])
        
        
        self.init_table(self.tableOrdClient)
        self.init_table(self.tableOrdClient_2)
        self.init_table(self.tableOrdClientSelect)
        
        PrinterClient.HEADER[indexClient] = PrinterClient.HEADER_CLIENT_TMP[indexClient]
        PrinterClient.HEADER[indexClient] = re.sub("^ ", '>', PrinterClient.HEADER[indexClient])

        self.tableOrdClient.add_rows([PrinterClient.HEADER_CLIENT_2])
        self.tableOrdClient_2.add_rows([PrinterClient.HEADER_CLIENT_2])
        self.tableOrdClientSelect.add_rows([PrinterClient.HEADER_CLIENT_2])
    
    
    
    def init_table(self, table):
        table.set_deco(Texttable.HEADER)
        table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
    
    
    def add_rows(self, tup, index):
        if index == 0:
            self.tableOrdClientSelect.add_rows(tup, False)
            self.selected = 1
        elif index == 1:
            self.tableOrdClient.add_rows(tup, False)
            self.dimTableClient += 1
        elif index == 2:
            self.tableOrdClient_2.add_rows(tup, False)
            self.dimTableClient_2 += 1
        elif index == 3:
            self.tableInfo.add_rows(tup,False)
            self.dimTableInfo += 1
        
    
    def setMyPadPos(self, mypad_pos):
        self.mypad_pos_client = mypad_pos

    def setIndexCursor(self, indexCursor):
        self.indexCursor = indexCursor


