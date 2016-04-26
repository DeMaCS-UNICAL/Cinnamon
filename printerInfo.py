#!/usr/bin/python

import sys, time, os, operator
import threading, curses, subprocess
import texttable
import re

import printerF
import printerClient
import printerAP

from time import sleep
from texttable import Texttable, get_color_string, bcolors

class PrinterInfo (threading.Thread):
    
    COLUMN_SIZE = 15
    COLUMN_SIZE_AP = 16
    
    HEIGHT_TABLE_CLIENT = 25
    HEIGHT_TABLE_AP = 25
    
    
    HEADER_CLIENT = [' STATION             ', ' AUTH',' DEAUTH ', ' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR%',' DATA  ',' RTS ',' CTS ',' ACK',' BEACON  ', ' PROBE_REQ  ', ' TOT_PACK']
    
    HEADER_AP = [' ESSID               ',' BSSID             ',' AUTH ',' DEAUTH ',' PWR ',' HAND_SUCC ',' HAND_FAIL ',' CORRUPT ',' CORR% ',' DATA ',' RTS ',' CTS ',' ACK ',' BEACON ', ' PROBE_REQ ', ' TOT_PACK']
    
    HEADER_INFO = ['ESSID               ','BSSID            ','STATION          ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK']
    

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.table = texttable.Texttable()
        self.tableAP = texttable.Texttable()

        self.info = {}
        self.infoAP = {}
        self.infoClient = {}
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
        self.endSniffOffline = False
        self.increase = 0
        
        self.src = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.src.nodelay(1)
        #curses.endwin()
        self.srcHeight = 50
        self.mypad_pos_client = 0
        self.mypad_pos_ap = 0
        
        curses.start_color()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        
        self.printerClient = printerClient.PrinterClient(self.srcHeight)
        self.printerAP = printerAP.PrinterAP(self.srcHeight)
        
        self.printerAP.createTable(self.indexOrdAP)
        self.printerClient.createTable(PrinterInfo.HEADER_INFO, self.indexOrdClient)
        
    
    def run(self):
        while (not self.stopSniff):
            
            cmd = self.src.getch()
            if not self.pauseSniff:
                self.printerClient.clear()
                self.printerAP.clear()
                
                self.printerClient.drawTable()
                self.printerAP.drawTable()
                
                self.printerClient.refreshTable()
                self.printerAP.refreshTable()

                if cmd == ord('s'):
                    if self.indexTable == 0:
                        if self.indexCursorClient == 2:
                            self.mypad_pos_client = 0
                        if self.indexCursorClient < len(self.infoClient) -1:
                            self.indexCursorClient += 1
                            self.printerClient.setIndexCursor(1, 1)
                            if not self.pressedInfo:
                                if self.indexCursorClient > PrinterInfo.HEIGHT_TABLE_CLIENT - 2:
                                    self.mypad_pos_client += 1
                            #else:
                                #if self.indexCursorClient + self.contInfoClient +4 > self.srcHeight:
                                    #self.printerClient.resizeTable(self.srcHeight+ self.contInfoClient +4)
                                #if self.indexCursorClient >= PrinterInfo.HEIGHT_TABLE_CLIENT - self.contInfoClient - 4:
                                    #if self.mypad_pos_client + self.contInfoClient < PrinterInfo.HEIGHT_TABLE_CLIENT:
                                        #self.mypad_pos_client = self.mypad_pos_client + self.contInfoClient
                                    #else:
                                        #self.printerClient.resizeTable(self.srcHeight+ self.contInfoClient +4)
                                        #self.mypad_pos_client = self.mypad_pos_client + self.contInfoClient
                            self.printerClient.setMyPadPos(self.mypad_pos_client)
                            self.printerClient.refreshTable()
                    else:
                        if self.indexCursorAP == 2:
                            self.mypad_pos_ap = 0
                        if self.indexCursorAP < len(self.infoAP) -1:
                            self.indexCursorAP += 1
                            self.printerAP.setIndexCursor(1, 1)
                                
                            if self.indexCursorAP > PrinterInfo.HEIGHT_TABLE_AP - 2:
                                self.mypad_pos_ap += 1
                                
                            self.printerAP.setMyPadPos(self.mypad_pos_ap)
                            self.printerAP.refreshTable()
                        
                elif cmd == ord('w'):
                    if self.indexTable == 0:
                        if self.indexCursorClient > 0:
                            self.indexCursorClient -= 1
                            self.printerClient.setIndexCursor(1, 2)
                            if self.indexCursorClient > 2:
                                if not self.pressedInfo:
                                    self.mypad_pos_client -= 1
                                
                                else: 
                                    self.mypad_pos_client -= self.contInfoClient
                            
                            self.printerClient.setMyPadPos(self.mypad_pos_client)
                            self.printerClient.refreshTable()
                            self.mypad_pos_client += self.contInfoClient - 1
                            if self.indexCursorClient <= 2:
                                self.mypad_pos_client = 0
                            self.printerClient.setMyPadPos(self.mypad_pos_client)
                    else:
                        if self.indexCursorAP > 0:
                            self.indexCursorAP -= 1
                            self.printerAP.setIndexCursor(1, 2)
                                
                            if self.indexCursorAP > 2:
                                self.mypad_pos_ap -= 1
                                
                            self.printerAP.setMyPadPos(self.mypad_pos_ap)
                            self.printerAP.refreshTable()
                        
                elif cmd == ord('+'):
                    if self.indexCursorClient + self.contInfoClient +4 > self.srcHeight:
                        self.printerClient.resizeTable(self.srcHeight+ self.contInfoClient +4)

                    self.pressedInfo = True
                    self.printerClient.setPressedInfo(self.pressedInfo)
                    self.contInfoClient = 0
                    self.printerClient.setContInfoClient(0, 0)
                    noRepeat = {}
                    
                    if self.pressedInfo:
                        for elem in self.info:
                            if self.tupl and (elem[0], self.tupl[0][0]) in self.info:
                                i = self.info[(elem[0], self.tupl[0][0])]
                                tup = tuple([[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16]]])

                                noRepeat[tup[0][0], tup[0][1]] = tup
                        for e in noRepeat:
                            self.printerClient.add_rows(noRepeat[e], 3)
                            self.contInfoClient += 1
                            self.printerClient.setContInfoClient(1, 1)
                            
                elif cmd == ord('-'):
                    self.contInfoClient = 0
                    self.printerClient.setContInfoClient(0, 0)
                    self.pressedInfo = False
                    self.printerClient.setPressedInfo(self.pressedInfo)
                    
                elif cmd == ord('>'):
                    if self.indexTable == 0:
                        if self.indexOrdClient < PrinterInfo.COLUMN_SIZE - 1:
                            self.printerClient.resetHeaderIndex(self.indexOrdClient)
                            self.indexOrdClient += 1
                    else:
                        if self.indexOrdAP < PrinterInfo.COLUMN_SIZE_AP - 1:
                            self.printerAP.resetHeaderIndex(self.indexOrdAP)
                            self.indexOrdAP += 1
                        
                elif cmd == ord('<'):
                    if self.indexTable == 0:
                        if self.indexOrdClient > 0:
                            self.printerClient.resetHeaderIndex(self.indexOrdClient)
                            self.indexOrdClient -= 1
                    else:
                        if self.indexOrdAP > 0:
                            self.printerAP.resetHeaderIndex(self.indexOrdAP)
                            self.indexOrdAP -= 1
                elif cmd == ord('t'):
                    if self.indexTable == 0:
                        self.indexTable = 1
                    else:
                        self.indexTable = 0
                elif cmd == ord('p'):
                    self.pauseSniff = True
                elif cmd == ord('q'):
                    curses.endwin()
                    self.stopSniff = True
                    
                if self.endSniffOffline:
                    self.printInformation()
            else:
                if cmd == ord('p'):
                    self.pauseSniff = False
            #self.src.refresh()
    
    
    
    def endOfflineSniff(self, endSniffOffline):
        self.endSniffOffline = endSniffOffline
    
    def sort_tableClient(self, col=0):
        if col != 0 and col != 3:
            return sorted(self.table, key=operator.itemgetter(col), cmp=self.numericCompair)
        else:
            return sorted(self.table, key=operator.itemgetter(col))

    def sort_tableAP(self, col=0):
        if col != 0 and col != 1 and col != 4:
            return sorted(self.tableAP, key=operator.itemgetter(col), cmp=self.numericCompair)
        else:
            return sorted(self.tableAP, key=operator.itemgetter(col))
    
    def numericCompair(self, x, y):
        return int(x) - int(y)

    
    def addInfo(self,i):
        if i[0] != "-" and i[0] != None:
            self.essid[(i[1],i[2])] = i[0]
        if (i[1],i[2]) not in self.info:
            self.info[(i[1],i[2])] = i
            self.index += 1
        else:
            if i[0] == "-" and (i[1],i[2]) in self.essid and self.essid[(i[1],i[2])] != "":
                j = tuple([self.essid[(i[1],i[2])], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16]])
                self.info[(i[1],i[2])] = j
            else:
                self.info[(i[1],i[2])] = i
               
        self.printInformation()
        
    def addInfoAP(self,i):
        if i[0] != "-" and i[0] != None:
            self.essid[(i[1],i[2])] = i[0]
        if (i[1],i[2]) not in self.info:
            self.infoAP[i[1]] = i
            self.index += 1
        else:
            if i[0] == "-" and (i[1],i[2]) in self.essid and self.essid[(i[1],i[2])] != "":
                j = tuple([self.essid[(i[1],i[2])], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16]])
                self.infoAP[i[1]] = j
            else:
                self.infoAP[i[1]] = i

        self.printInformation()
        
    def addInfoClient(self,i):
        if i[0] != "-" and i[0] != None:
            self.essid[(i[1],i[2])] = i[0]
        if (i[1],i[2]) not in self.info:
            self.infoClient[i[2]] = i
            self.index += 1
        else:
            if i[0] == "-" and (i[1],i[2]) in self.essid and self.essid[(i[1],i[2])] != "":
                j = tuple([self.essid[(i[1],i[2])], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16]])
                self.infoClient[i[2]] = j
            else:
                self.infoClient[i[2]] = i
                
        self.printInformation()


    def printInformation(self):
        #self.tupl = []
        self.table.reset()
        self.tableAP.reset()
        
        self.printerClient.reset()
        self.printerAP.reset()
        
        self.createTable(PrinterInfo.HEADER_CLIENT, PrinterInfo.HEADER_AP)
        
        self.printerAP.createTable(self.indexOrdAP)
        self.printerClient.createTable(PrinterInfo.HEADER_INFO, self.indexOrdClient)
        
        noRepeat = {}
        
        if self.pressedInfo:
            self.contInfoClient = 0
            self.printerClient.setContInfoClient(0, False)
            for elem in self.info:
                if self.tupl and (elem[0], self.tupl[0][0]) in self.info:
                    i = self.info[(elem[0], self.tupl[0][0])]
                    tup = tuple([[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16]]])

                    noRepeat[tup[0][0], tup[0][1]] = tup
            for e in noRepeat:
                self.printerClient.add_rows(noRepeat[e], 3)
                self.contInfoClient += 1
                self.printerClient.setContInfoClient(1, 1)
        
        for i in self.infoAP:
            tup2 = tuple([self.infoAP[i][0], self.infoAP[i][1], self.infoAP[i][3], self.infoAP[i][4], self.infoAP[i][5], self.infoAP[i][6], self.infoAP[i][7], self.infoAP[i][8], self.infoAP[i][9], self.infoAP[i][10], self.infoAP[i][11], self.infoAP[i][12], self.infoAP[i][13], self.infoAP[i][14], self.infoAP[i][15], self.infoAP[i][16]])
            self.tableAP.add_rows([tup2],False)
        
        for i in self.infoClient:
            tup1 = tuple([self.infoClient[i][2], self.infoClient[i][3], self.infoClient[i][4], self.infoClient[i][5], self.infoClient[i][6], self.infoClient[i][7], self.infoClient[i][8], self.infoClient[i][9], self.infoClient[i][10], self.infoClient[i][11], self.infoClient[i][12], self.infoClient[i][13], self.infoClient[i][14], self.infoClient[i][15], self.infoClient[i][16]])
            
            self.table.add_rows([tup1],False)
        
        c = 0
        for i in self.sort_tableClient(self.indexOrdClient):
            a = i[0].rstrip('\n').split(','), i[1].rstrip('\n').split(','), i[2].rstrip('\n').split(','), i[3].rstrip('\n').split(','), i[4].rstrip('\n').split(','), i[5].rstrip('\n').split(','), i[6].rstrip('\n').split(','), i[7].rstrip('\n').split(','), i[8].rstrip('\n').split(','), i[9].rstrip('\n').split(','), i[10].rstrip('\n').split(','), i[11].rstrip('\n').split(','), i[12].rstrip('\n').split(','), i[13].rstrip('\n').split(','), i[14].rstrip('\n').split(',')
                
            perc = a[7][0]+"%"
            
            tup = tuple([[a[0][0], a[1][0], a[2][0], a[3][0], a[4][0], a[5][0], a[6][0], perc, a[8][0], a[9][0], a[10][0], a[11][0], a[12][0], a[13][0], a[14][0]]])
            if c < self.printerClient.getIndexCursor():
                self.printerClient.add_rows(tup, 1)
                c += 1
            elif c > self.printerClient.getIndexCursor():
                self.printerClient.add_rows(tup, 2)
                c += 1
            else:
                self.tupl = tup
                self.printerClient.add_rows(self.tupl, 0)
                c += 1
        
        d = 0
        for i in self.sort_tableAP(self.indexOrdAP):
            a = i[0].rstrip('\n').split(','), i[1].rstrip('\n').split(','), i[2].rstrip('\n').split(','), i[3].rstrip('\n').split(','), i[4].rstrip('\n').split(','), i[5].rstrip('\n').split(','), i[6].rstrip('\n').split(','), i[7].rstrip('\n').split(','), i[8].rstrip('\n').split(','), i[9].rstrip('\n').split(','), i[10].rstrip('\n').split(','), i[11].rstrip('\n').split(','), i[12].rstrip('\n').split(','), i[13].rstrip('\n').split(','), i[14].rstrip('\n').split(','), i[15].rstrip('\n').split(',')

            perc = a[8][0]+"%"

            tup = tuple([[a[0][0], a[1][0], a[2][0], a[3][0], a[4][0], a[5][0], a[6][0], a[7][0], perc, a[9][0], a[10][0], a[11][0], a[12][0], a[13][0], a[14][0], a[15][0]]])
            if d < self.printerAP.getIndexCursor():
                self.printerAP.add_rows(tup, 1)
                d += 1
            elif d > self.printerAP.getIndexCursor():
                self.printerAP.add_rows(tup, 2)
                d += 1
            else:
                self.printerAP.add_rows(tup, 0)
                d += 1
            


    def createTable(self, header_client, header_ap):
        self.tableAP.set_deco(Texttable.HEADER)
        self.tableAP.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableAP.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableAP.add_rows([[header_ap[0], header_ap[1], header_ap[2], header_ap[3], header_ap[4], header_ap[5], header_ap[6], header_ap[7], header_ap[8], header_ap[9], header_ap[10], header_ap[11], header_ap[12], header_ap[13],  header_ap[14], header_ap[15]]])


        self.table.set_deco(Texttable.HEADER)
        self.table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.table.add_rows([[header_client[0], header_client[1], header_client[2], header_client[3], header_client[4], header_client[5], header_client[6], header_client[7], header_client[8], header_client[9], header_client[10], header_client[11], header_client[12],  header_client[13], header_client[14]]])
        

    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
