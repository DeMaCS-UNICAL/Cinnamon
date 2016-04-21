#!/usr/bin/python

import sys, time, os, socket, operator
import threading, curses
import texttable
import select

from time import sleep
from texttable import Texttable, get_color_string, bcolors

class PrinterInfo (threading.Thread):
    
    COLUMN_SIZE = 15
    COLUMN_SIZE_AP = 16
    
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.table = texttable.Texttable()
        self.tableOrdClient = texttable.Texttable()
        self.tableAP = texttable.Texttable()
        self.tableOrdAP = texttable.Texttable()
        self.info = {}
        self.infoAP = {}
        self.infoClient = {}
        self.index = 0
        
        self.createtableAP('ESSID                 ','BSSID            ','AUTH','DEAUTH','PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK', bcolors.BLUE)
       
        self.createTableClient('STATION          ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK', bcolors.BLUE)
        
        #self.createTable('ESSID                 ','BSSID            ','STATION          ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK', bcolors.BLUE)
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)
        self.essid = {}
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.stopSniff = False
        self.pauseSniff = False
        self.indexOrdAP = 0
        self.indexOrdClient = 0
        self.indexTable = 0
        
        self.src = curses.initscr()
        curses.noecho()
        #curses.endwin()
        self.srcHeight = 50
        self.mypad_pos = 0
        
        self.src = curses.newpad(self.srcHeight,300)
        
        self.src.nodelay(1)
        self.src.keypad(True)
        self.src.insstr(0,0, self.tableOrdClient.draw())

        #self.srctableAP = curses.initscr()
        self.srcHeight = 50
        self.mypad_pos = 0
        
        self.srctableAP = curses.newpad(self.srcHeight,300)
        
        self.srctableAP.nodelay(1)
        self.srctableAP.keypad(True)
        self.srctableAP.insstr(0, 0, self.tableOrdClient.draw())
        #self.cmd = None
        
    
    #def updateGetch(self):
        ##while (True):
        #self.cmd = self.src.getch()
    
    
    def run(self):
        
        while (not self.stopSniff):
            #print ""
            #self.printInformation()
            cmd = self.src.getch()
            if not self.pauseSniff:
                self.src.clear()
                self.srctableAP.clear()
                #self.src.resize(self.srcHeight+100, 300)
                self.src.insstr(0, 0, self.tableOrdClient.draw())
                self.srctableAP.insstr(0, 0, self.tableOrdAP.draw())
                
                self.src.refresh(self.mypad_pos, 0, 0, 0, 25, 190)
                self.srctableAP.refresh(0,0, 29,0, 50,190)
                
                #if cmd == curses.KEY_UP:
                #if  cmd == self.src.keypad(1):
                if cmd == ord('s'):
                    self.mypad_pos += 10
                    #self.src.move(mypad_pos,0)
                    self.src.refresh(self.mypad_pos, 0, 0, 0, 20, 190)
                #if cmd == curses.KEY_DOWN:
                elif cmd == ord('w'):
                #elif cmd == self.src.keypad(4):
                    self.mypad_pos -= 10
                    self.src.refresh(self.mypad_pos, 0, 0, 0, 20, 190)
                elif cmd == ord('>'):
                    if self.indexTable == 0:
                        if self.indexOrdClient < PrinterInfo.COLUMN_SIZE - 1:
                            self.indexOrdClient += 1
                    else:
                        if self.indexOrdAP < PrinterInfo.COLUMN_SIZE_AP - 1:
                            self.indexOrdAP += 1
                        
                elif cmd == ord('<'):
                    if self.indexTable == 0:
                        if self.indexOrdClient > 0:
                            self.indexOrdClient -= 1
                    else:
                        if self.indexOrdAP > 0:
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
            else:
                if cmd == ord('p'):
                    self.pauseSniff = False
            #self.src.refresh()
    
    
    def sort_tableClient(self, col=0):
        return sorted(self.table, key=operator.itemgetter(col))
    
    def sort_tableAP(self, col=0):
        return sorted(self.tableAP, key=operator.itemgetter(col))
    
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
                #self.table.add_rows([j])
            else:
                self.info[(i[1],i[2])] = i
                #self.table.add_rows([i])
                
        #self.src.refresh()
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
                #self.table.add_rows([j])
            else:
                self.infoAP[i[1]] = i
                #self.table.add_rows([i])
                
        #self.src.refresh()
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
                #self.table.add_rows([j])
            else:
                self.infoClient[i[2]] = i
                #self.table.add_rows([i])
                
        #self.src.refresh()
        self.printInformation()


    def printInformation(self):
        self.table.reset()
        self.tableAP.reset()
        self.tableOrdClient.reset()
        self.tableOrdAP.reset()
        self.createtableAP('ESSID                 ','BSSID            ','AUTH','DEAUTH','PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK', bcolors.BLUE)
       
        self.createTableClient('STATION          ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON', 'PROBE_REQ', 'TOT_PACK', bcolors.BLUE)
       
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)
        #sorted(self.info)
        
        #sorted(self.info, key=lambda x:x[1][13])
        
        #b = self.info.items()
        #b.sort(key=lambda x:x[0])  # sorting by the third item in the tuple
        #print b
        #b.sort(self.info.keys(), key=lambda x: self.info[x][1], reverse=True)
        #for i in b:
            #print b[i]
        for i in self.infoAP:
            ##print self.info[i]
            ##sorted(self.info[i],key=lambda x:-x[2])
            tup2 = tuple([self.infoAP[i][0], self.infoAP[i][1], self.infoAP[i][3], self.infoAP[i][4], self.infoAP[i][5], self.infoAP[i][6], self.infoAP[i][7], self.infoAP[i][8], self.infoAP[i][9], self.infoAP[i][10], self.infoAP[i][11], self.infoAP[i][12], self.infoAP[i][13], self.infoAP[i][14], self.infoAP[i][15], self.infoAP[i][16]])
            self.tableAP.add_rows([tup2],False)
        
        for i in self.infoClient:
            tup1 = tuple([self.infoClient[i][2], self.infoClient[i][3], self.infoClient[i][4], self.infoClient[i][5], self.infoClient[i][6], self.infoClient[i][7], self.infoClient[i][8], self.infoClient[i][9], self.infoClient[i][10], self.infoClient[i][11], self.infoClient[i][12], self.infoClient[i][13], self.infoClient[i][14], self.infoClient[i][15], self.infoClient[i][16]])
            
            self.table.add_rows([tup1],False)
        
        for i in self.sort_tableClient(self.indexOrdClient):
            a = i[0].rstrip('\n').split(','), i[1].rstrip('\n').split(','), i[2].rstrip('\n').split(','), i[3].rstrip('\n').split(','), i[4].rstrip('\n').split(','), i[5].rstrip('\n').split(','), i[6].rstrip('\n').split(','), i[7].rstrip('\n').split(','), i[8].rstrip('\n').split(','), i[9].rstrip('\n').split(','), i[10].rstrip('\n').split(','), i[11].rstrip('\n').split(','), i[12].rstrip('\n').split(','), i[13].rstrip('\n').split(','), i[14].rstrip('\n').split(',')
            #b = i.split(',')
            #tup = ()
            tup = tuple([[a[0][0], a[1][0], a[2][0], a[3][0], a[4][0], a[5][0], a[6][0], a[7][0], a[8][0], a[9][0], a[10][0], a[11][0], a[12][0], a[13][0], a[14][0]]])
            self.tableOrdClient.add_rows(tup,False)
        
        for i in self.sort_tableAP(self.indexOrdAP):
            a = i[0].rstrip('\n').split(','), i[1].rstrip('\n').split(','), i[2].rstrip('\n').split(','), i[3].rstrip('\n').split(','), i[4].rstrip('\n').split(','), i[5].rstrip('\n').split(','), i[6].rstrip('\n').split(','), i[7].rstrip('\n').split(','), i[8].rstrip('\n').split(','), i[9].rstrip('\n').split(','), i[10].rstrip('\n').split(','), i[11].rstrip('\n').split(','), i[12].rstrip('\n').split(','), i[13].rstrip('\n').split(','), i[14].rstrip('\n').split(','), i[15].rstrip('\n').split(',')
            #b = i.split(',')
            #tup = ()
            tup = tuple([[a[0][0], a[1][0], a[2][0], a[3][0], a[4][0], a[5][0], a[6][0], a[7][0], a[8][0], a[9][0], a[10][0], a[11][0], a[12][0], a[13][0], a[14][0], a[15][0]]])
            self.tableOrdAP.add_rows(tup,False)

            
                    
                
        #for w in sorted(self.info, key=self.info.get, reverse=True):
            #print w, self.info[w]
                
        #self.src.addstr(self.table.draw() + "\n")
        
    def createtableAP(self,essid, bssid, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, probe_req, tot_pack, color):
        self.tableAP.set_deco(Texttable.HEADER)
        self.tableAP.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableAP.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableOrdAP.set_deco(Texttable.HEADER)
        self.tableOrdAP.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableOrdAP.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
        self.tableAP.add_rows([[essid, bssid, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon,  probe_req, tot_pack]])
        self.tableOrdAP.add_rows([[essid, bssid, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon,  probe_req, tot_pack]])
        #self.src.refresh()
        #print(self.table.draw() + "\n")

    def createTableClient(self, station, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, probe_req, tot_pack, color):
        self.table.set_deco(Texttable.HEADER)
        self.table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        
        self.tableOrdClient.set_deco(Texttable.HEADER)
        self.tableOrdClient.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableOrdClient.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
        self.table.add_rows([[station, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon,  probe_req, tot_pack]])
        self.tableOrdClient.add_rows([[station, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon,  probe_req, tot_pack]])

    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
