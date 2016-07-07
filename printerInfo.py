#!/usr/bin/python

import sys, os, operator
import threading, curses
import texttable
import printerF
import printerClient
import printerAP
import printerHelp

from texttable import Texttable

class PrinterInfo ():
    
    COLUMN_SIZE = 21
    COLUMN_SIZE_AP = 21
    
    HEIGHT_TABLE_CLIENT = 21
    HEIGHT_TABLE_AP = 25
    
    
    HEADER_CLIENT = [' STATION'+" "*13, 'CH', ' AUT',' DEAUT ', ' ASS_RQ ',' ASS_RP ',' DISASS ',' HAND_S ',' HAND_F ',' CORR  ',' CORR% ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC  ', ' PROBE_PQ  ', ' PROBE_RP  ', ' TOT_PACK', ' OTHER', 'CONT']
    
    HEADER_AP = [' ESSID'+" "*18,' BSSID'+" "*13, ' CH ', ' AUT ',' DEAUT ',' ASS_RQ ',' ASS_RP ',' DIS ',' HAND_S ',' HAND_F ',' PWR ',' CORR ',' CORR% ',' DATA ',' RTS  ',' CTS  ',' ACK ',' BEAC ', ' PROBE_PQ', ' PROBE_RP ', ' TOT_PACK']
    
    HEADER_INFO = ['ESSID'+" "*15,'BSSID'+" "*12,'AUT','DEAUT', 'ASS_RQ','ASS_RP','DISASS','HAND_S','HAND_F','PWR','CORR','CORR%','DATA','RTS ','CTS ','ACK ','BEAC','PROBE_PQ','PROBE_RP','TOT_PACK']
    

    def __init__(self, threadID, name, delay):
        self.table = texttable.Texttable()
        self.tableAP = texttable.Texttable()

        self.info = {}
        self.infoAP = {}
        self.infoClient = {}

        self.info_pause = {}
        self.infoAP_pause = {}
        self.infoClient_pause = {}
        
        self.index = 0
        self.indexOrdAP = 0
        self.indexOrdClient = 0
        
        self.indexCursorClient = 0
        self.indexCursorAP = 0
        self.contInfoClient = 0
        
        self.createTable(PrinterInfo.HEADER_CLIENT, PrinterInfo.HEADER_AP)

        self.essid = {}
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.stopSniff = False
        self.pauseSniff = False
        self.indexTable = 0
        
        self.tupl = []
        
        self.pressedInfo = False
        self.reverseOrder_client = False
        self.reverseOrder_ap = False
        self.endSniffOffline = False
        self.increase = 0
        
        self.srcHeight = 50
        self.mypad_pos_client = 0
        self.mypad_pos_ap = 0
        
        self.chooseMacClient = ""
        
        #self.lock = threading.Lock()
        
        curses.initscr()
        #curses.noecho()
        #curses.cbreak()
        
        #LINES, COL = src.getmaxyx()
        #LINES = 60
        #t = open("H.txt","a")
        #t.write(str(LINES)+" "+str(COL)+"\n")
        #t.close()
        #curses.resizeterm(55, 195)
        
        #curses.curs_set(0)
        
        curses.start_color()
        
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        
        
        self.printerClient = printerClient.PrinterClient(self.srcHeight+10)
        self.printerAP = printerAP.PrinterAP(self.srcHeight+10)
        self.printerHelp = printerHelp.PrinterHelp(self.srcHeight+10)
        
        self.printerAP.createTable(self.indexOrdAP)
        self.printerClient.createTable(PrinterInfo.HEADER_INFO, self.indexOrdClient)
        
        #self.f = open('/dev/null', 'w')
    
    
    def reverseOrderTable(self):
        if self.indexTable == 0:
            if self.reverseOrder_client == True:
                self.reverseOrder_client = False
            else:
                self.reverseOrder_client = True
        else:
            if self.reverseOrder_ap == True:
                self.reverseOrder_ap = False
            else:
                self.reverseOrder_ap = True
    
    def changeTable(self):
        if self.indexTable == 0:
            self.indexTable = 1
        else:
            self.indexTable = 0
    
    def goDown(self):
        if self.indexTable == 0:
            infoClient_tmp = {}
            if not self.pauseSniff:
                info_tmp = self.infoClient
            else:
                info_tmp = self.infoClient_pause
            
            if self.indexCursorClient < 2:
                self.mypad_pos_client = 0
            if self.indexCursorClient < len(info_tmp) -1:
                self.indexCursorClient += 1
                self.printerClient.setIndexCursor(self.indexCursorClient)

                if not self.pressedInfo:
                    if self.indexCursorClient > PrinterInfo.HEIGHT_TABLE_CLIENT + self.mypad_pos_client:
                        self.mypad_pos_client += PrinterInfo.HEIGHT_TABLE_CLIENT - 1
                else:
                    if self.indexCursorClient + self.contInfoClient + 5 > PrinterInfo.HEIGHT_TABLE_CLIENT + self.mypad_pos_client:
                        self.mypad_pos_client += PrinterInfo.HEIGHT_TABLE_CLIENT - 1 + self.contInfoClient - 5

                self.printerClient.setMyPadPos(self.mypad_pos_client)
        else:
            if self.indexCursorAP == 2:
                self.mypad_pos_ap = 0
            if self.indexCursorAP < len(self.infoAP) -1:
                self.indexCursorAP += 1
                self.printerAP.setIndexCursor(self.indexCursorAP)
                    
                if self.indexCursorAP > PrinterInfo.HEIGHT_TABLE_AP - 2:
                    self.mypad_pos_ap += 1
                    
            self.printerAP.setMyPadPos(self.mypad_pos_ap)
        
    
    def goUp(self):
        if self.indexTable == 0:
            if self.indexCursorClient > 0:
                self.indexCursorClient -= 1
                self.printerClient.setIndexCursor(self.indexCursorClient)
                
                if self.indexCursorClient <= self.mypad_pos_client:
                    if not self.pressedInfo:
                        self.mypad_pos_client -= PrinterInfo.HEIGHT_TABLE_CLIENT - 1
                    else:
                        self.mypad_pos_client -= PrinterInfo.HEIGHT_TABLE_CLIENT - 1 - self.contInfoClient
                        
                self.printerClient.setMyPadPos(self.mypad_pos_client)
        else:
            if self.indexCursorAP > 0:
                self.indexCursorAP -= 1
                self.printerAP.setIndexCursor(self.indexCursorAP)
                    
                if self.indexCursorAP > 2:
                    self.mypad_pos_ap -= 1
                    
                self.printerAP.setMyPadPos(self.mypad_pos_ap)


    def plusInfo(self):
        if self.indexTable == 0:
            self.pressedInfo = True
            self.printerClient.setPressedInfo(self.pressedInfo)
            self.contInfoClient = 0
            #self.printerClient.setContInfoClient(self.contInfoClient)
            noRepeat = {}
            
            if self.pressedInfo:
                info_tmp = {}
                if not self.pauseSniff:
                    info_tmp = self.info
                else:
                    info_tmp = self.info_pause
                for elem in info_tmp:
                    if self.tupl and (elem[0], self.tupl[0][0]) in info_tmp:
                        i = info_tmp[(elem[0], self.tupl[0][0])]
                        perc = i[12]+"%"
                        tup = tuple([[i[0], i[1], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], perc, i[13], i[14], i[15], i[16], i[17], i[18], i[19], i[20]]])

                        noRepeat[tup[0][0], tup[0][1]] = tup
                for e in noRepeat:
                    self.printerClient.add_rows(noRepeat[e], 3)
                    self.contInfoClient += 1
                    self.printerClient.setContInfoClient(self.contInfoClient)
    
    def removeInfo(self):
        #self.printerClient.clear()
        if self.indexTable == 0:
            #self.printerClient.cleanRow()
            self.contInfoClient = 0
            self.printerClient.setContInfoClient(self.contInfoClient)
            self.pressedInfo = False
            self.printerClient.setPressedInfo(self.pressedInfo)
    
    def nextColumnOrd(self):
        if self.indexTable == 0:
            if self.indexOrdClient < PrinterInfo.COLUMN_SIZE - 1:
                self.printerClient.resetHeaderIndex(self.indexOrdClient)
                self.indexOrdClient += 1
                self.printerClient.setIndexHeader(self.indexOrdClient)
        else:
            if self.indexOrdAP < PrinterInfo.COLUMN_SIZE_AP - 1:
                self.printerAP.resetHeaderIndex(self.indexOrdAP)
                self.indexOrdAP += 1
                self.printerAP.setIndexHeader(self.indexOrdAP)

    def previousColumnOrd(self):
        if self.indexTable == 0:
            if self.indexOrdClient > 0:
                self.printerClient.resetHeaderIndex(self.indexOrdClient)
                self.indexOrdClient -= 1
                self.printerClient.setIndexHeader(self.indexOrdClient)
        else:
            if self.indexOrdAP > 0:
                self.printerAP.resetHeaderIndex(self.indexOrdAP)
                self.indexOrdAP -= 1
                self.printerAP.setIndexHeader(self.indexOrdAP)
        
    
    def update(self):
        if self.indexTable == 0:
            self.printerClient.setIsSelected(True)
            self.printerAP.setIsSelected(False)
        else:
            self.printerAP.setIsSelected(True)
            self.printerClient.setIsSelected(False)
        
        self.printerClient.refreshTable()
        self.printerAP.refreshTable()
        self.printerHelp.refreshTable()
        
        self.printerClient.resizeTable(self.srcHeight+ 100)
        self.printerAP.resizeTable(self.srcHeight+ 100)
        self.printerHelp.resizeTable(self.srcHeight+ 100)
        
        self.printerClient.drawTable()
        self.printerAP.drawTable()
        self.printerHelp.drawTable()
        
        
        if self.stopSniff:
            curses.endwin()
    
    def setPauseSniff(self, pauseSniff):
        self.pauseSniff = pauseSniff
        
    def getPauseSniff(self):
        return self.pauseSniff
    
    def endOfflineSniff(self, endSniffOffline):
        self.endSniffOffline = endSniffOffline
    
    def sort_tableClient(self, col=0):
        if col != 0 and col != 1 and col != 7:
            if self.reverseOrder_client:
                return sorted(self.table, key=operator.itemgetter(col), cmp=self.numericCompair, reverse = True)
            else:
                return sorted(self.table, key=operator.itemgetter(col), cmp=self.numericCompair)
        else:
            if self.reverseOrder_client:
                return sorted(self.table, key=operator.itemgetter(col), reverse = True)
            else:
                return sorted(self.table, key=operator.itemgetter(col))

    def sort_tableAP(self, col=0):
        if col != 0 and col != 1 and col != 10:
            if self.reverseOrder_ap:
                return sorted(self.tableAP, key=operator.itemgetter(col), cmp=self.numericCompair, reverse = True)
            else:
                return sorted(self.tableAP, key=operator.itemgetter(col), cmp=self.numericCompair)
        else:
            if self.reverseOrder_ap:
                return sorted(self.tableAP, key=operator.itemgetter(col), reverse = True)
            else:
                return sorted(self.tableAP, key=operator.itemgetter(col))
    
    def numericCompair(self, x, y):
        return int(x) - int(y)

    
    def addInfo(self, i):
        self.info = i
        #self.printInformation()
        
    def addInfoAP(self, i):
        self.infoAP = i
        #self.printInformation()
        
    def addInfoClient(self, i):
        self.infoClient = i
        #self.printInformation()

    def setChooseMacAddress(self, macAddressClient):
        self.chooseMacClient = macAddressClient
    
    def sortTable(self, info, infoAP, infoClient):
        self.table.reset()
        self.tableAP.reset()
        
        self.printerClient.reset()
        self.printerAP.reset()
        
        self.createTable(PrinterInfo.HEADER_CLIENT, PrinterInfo.HEADER_AP)
        
        for i in infoAP.keys():
            essid = infoAP[i][0]
            if essid == "":
                essid = "-"
            tup2 = tuple([essid, infoAP[i][1], infoAP[i][3], infoAP[i][4], infoAP[i][5], infoAP[i][6], infoAP[i][7], infoAP[i][8], infoAP[i][9], infoAP[i][10], infoAP[i][11], infoAP[i][12], infoAP[i][13], infoAP[i][14], infoAP[i][15], infoAP[i][16], infoAP[i][17], infoAP[i][18], infoAP[i][19], infoAP[i][20], infoAP[i][21]])
            self.tableAP.add_rows([tup2],False)
        
        if self.chooseMacClient == "":
            for i in infoClient.keys():
                tup1 = tuple([infoClient[i][2], infoClient[i][3], infoClient[i][4], infoClient[i][5], infoClient[i][6], infoClient[i][7], infoClient[i][8], infoClient[i][9], infoClient[i][10], infoClient[i][11], infoClient[i][12], infoClient[i][13], infoClient[i][14], infoClient[i][15], infoClient[i][16], infoClient[i][17], infoClient[i][18], infoClient[i][19], infoClient[i][20], infoClient[i][21]])
                
                self.table.add_rows([tup1],False)
        else:
            i = self.chooseMacClient
            tup1 = tuple([infoClient[i][2], infoClient[i][3], infoClient[i][4], infoClient[i][5], infoClient[i][6], infoClient[i][7], infoClient[i][8], infoClient[i][9], infoClient[i][10], infoClient[i][11], infoClient[i][12], infoClient[i][13], infoClient[i][14], infoClient[i][15], infoClient[i][16], infoClient[i][17], infoClient[i][18], infoClient[i][19], infoClient[i][20], infoClient[i][21]])
                
            self.table.add_rows([tup1],False)
            
        c = 0
        for i in self.sort_tableClient(self.indexOrdClient):
            i[10] += "%"
            
            tup = tuple([i])
            if tup != None:
                if c < self.printerClient.getIndexCursor():
                    self.printerClient.add_rows(tup, 1)
                elif c > self.printerClient.getIndexCursor():
                    self.printerClient.add_rows(tup, 2)
                else:
                    self.tupl = tup
                    self.printerClient.add_rows(self.tupl, 0)
                c += 1
        
            
        d = 0
        for i in self.sort_tableAP(self.indexOrdAP):
            i[12] += "%"
            
            tup = tuple([i])
            if tup != None:
                if d < self.printerAP.getIndexCursor():
                    self.printerAP.add_rows(tup, 1)
                elif d > self.printerAP.getIndexCursor():
                    self.printerAP.add_rows(tup, 2)
                else:
                    self.printerAP.add_rows(tup, 0)
                d += 1
                    
        noRepeat = {}
        
        if self.pressedInfo:
            self.contInfoClient = 0
            self.printerClient.setContInfoClient(self.contInfoClient)
            for elem in info.keys():
                if self.tupl and (elem[0], self.tupl[0][0]) in info:
                    i =info[(elem[0], self.tupl[0][0])]
                    perc = i[12]+"%"
                    tup = tuple([[i[0], i[1], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], perc, i[13], i[14], i[15], i[16], i[17], i[18], i[19], i[20]]])

                    noRepeat[tup[0][0], tup[0][1]] = tup
            for e in noRepeat:
                self.printerClient.add_rows(noRepeat[e], 3)
                self.contInfoClient += 1
                self.printerClient.setContInfoClient(self.contInfoClient)

        self.update()
        

    def printInformation(self):
        #self.lock.acquire()

        if self.pauseSniff:
            self.sortTable(self.info_pause, self.infoAP_pause, self.infoClient_pause)
        else:
            self.sortTable(self.info, self.infoAP, self.infoClient)
            
            self.info_pause = {k:v for k,v in self.info.items()}
            self.infoAP_pause = {k:v for k,v in self.infoAP.items()}
            self.infoClient_pause = {k:v for k,v in self.infoClient.items()}
        
        self.update()
        #self.lock.release()
    
    
    def createTable(self, header_client, header_ap):
        self.tableAP.set_deco(Texttable.HEADER)
        self.tableAP.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableAP.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableAP.add_rows([[header_ap[0], header_ap[1], header_ap[2], header_ap[3], header_ap[4], header_ap[5], header_ap[6], header_ap[7], header_ap[8], header_ap[9], header_ap[10], header_ap[11], header_ap[12], header_ap[13],  header_ap[14], header_ap[15], header_ap[16], header_ap[17], header_ap[18], header_ap[19], header_ap[20]]])


        self.table.set_deco(Texttable.HEADER)
        self.table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.table.add_rows([[header_client[0], header_client[1], header_client[2], header_client[3], header_client[4], header_client[5], header_client[6], header_client[7], header_client[8], header_client[9], header_client[10], header_client[11], header_client[12],  header_client[13], header_client[14], header_client[15], header_client[16], header_client[17], header_client[18], header_client[19]]])
        

    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff

    def getStopSniff(self):
        return self.stopSniff
