#!/usr/bin/python

import sys, time, os, socket, operator
import threading, curses
import texttable
import select

from time import sleep
from texttable import Texttable, get_color_string, bcolors

class PrinterInfo (threading.Thread):
    
    COLUMN_SIZE = 17
    
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.table = texttable.Texttable()
        self.tableOrd = texttable.Texttable()
        self.info = {}
        self.index = 0
        self.createTable('ESSID                 ','BSSID            ','STATION          ', 'PROBE_REQ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON','TOT_PACK', bcolors.BLUE)
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)
        self.essid = {}
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.stopSniff = False
        self.pauseSniff = False
        self.indexOrd = 0
        
        self.src = curses.initscr()
        curses.noecho()
        #curses.endwin()
        self.srcHeight = 10
        self.mypad_pos = 0
        
        self.src = curses.newpad(self.srcHeight,300)
        
        self.src.nodelay(1)
        self.src.keypad(True)
        self.src.insstr(0,0, self.tableOrd.draw())
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
                self.src.resize(self.srcHeight+100, 300)
                self.src.insstr(0, 0, self.tableOrd.draw())
                
                self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
                
                #if cmd == curses.KEY_UP:
                #if  cmd == self.src.keypad(1):
                if cmd == ord('s'):
                    self.mypad_pos += 10
                    #self.src.move(mypad_pos,0)
                    self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
                #if cmd == curses.KEY_DOWN:
                elif cmd == ord('w'):
                #elif cmd == self.src.keypad(4):
                    self.mypad_pos -= 10
                    self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
                elif cmd == ord('>'):
                    if self.indexOrd < PrinterInfo.COLUMN_SIZE - 1:
                        self.indexOrd += 1
                elif cmd == ord('<'):
                    if self.indexOrd > 0:
                        self.indexOrd -= 1
                elif cmd == ord('p'):
                    self.pauseSniff = True
                elif cmd == ord('q'):
                    curses.endwin()
                    self.stopSniff = True
            else:
                if cmd == ord('p'):
                    self.pauseSniff = False
            #self.src.refresh()
    
    
    def sort_table(self, col=0):
        return sorted(self.table, key=operator.itemgetter(col))
    
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


    def printInformation(self):
        self.table.reset()
        self.tableOrd.reset()
        self.createTable('ESSID                 ','BSSID            ','STATION          ','PROBE_REQ','AUTH','DEAUTH','PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON','TOT_PACK', bcolors.BLUE)
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)
        #sorted(self.info)
        
        #sorted(self.info, key=lambda x:x[1][13])
        
        #b = self.info.items()
        #b.sort(key=lambda x:x[0])  # sorting by the third item in the tuple
        #print b
        #b.sort(self.info.keys(), key=lambda x: self.info[x][1], reverse=True)
        #for i in b:
            #print b[i]
        for i in self.info:
            ##print self.info[i]
            ##sorted(self.info[i],key=lambda x:-x[2])
            self.table.add_rows([self.info[i]],False)
                
        for i in self.sort_table(self.indexOrd):
            a = i[0].rstrip('\n').split(','), i[1].rstrip('\n').split(','), i[2].rstrip('\n').split(','), i[3].rstrip('\n').split(','), i[4].rstrip('\n').split(','), i[5].rstrip('\n').split(','), i[6].rstrip('\n').split(','), i[7].rstrip('\n').split(','), i[8].rstrip('\n').split(','), i[9].rstrip('\n').split(','), i[10].rstrip('\n').split(','), i[11].rstrip('\n').split(','), i[12].rstrip('\n').split(','), i[13].rstrip('\n').split(','), i[14].rstrip('\n').split(','), i[15].rstrip('\n').split(','), i[16].rstrip('\n').split(',')
            #b = i.split(',')
            #tup = ()
            tup = tuple([[a[0][0], a[1][0], a[2][0], a[3][0], a[4][0], a[5][0], a[6][0], a[7][0], a[8][0], a[9][0], a[10][0], a[11][0], a[12][0], a[13][0], a[14][0], a[15][0], a[16][0]]])
            #print tup
            #tup = tuple([str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7]), str(i[8]), str(i[9]), str(i[10]), str(i[11]), str(i[12]), str(i[13]), str(i[14]), str(i[15]), str(i[16])])
            #for idx, elem in enumerate(row):
                #tup = tup + (elem,)
                #print idx, " ", elem
            self.tableOrd.add_rows(tup,False)
            #print row
            
                    
                
        #for w in sorted(self.info, key=self.info.get, reverse=True):
            #print w, self.info[w]
                
        #self.src.addstr(self.table.draw() + "\n")
        
    def createTable(self,essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, tot_pack, color):
        self.table.set_deco(Texttable.HEADER)
        self.table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        self.tableOrd.set_deco(Texttable.HEADER)
        self.tableOrd.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.tableOrd.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
        self.table.add_rows([[essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, tot_pack]])
        self.tableOrd.add_rows([[essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, tot_pack]])
        #self.src.refresh()
        #print(self.table.draw() + "\n")


    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
