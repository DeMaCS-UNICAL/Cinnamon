#!/usr/bin/python

import sys, time, os, socket
import threading, curses
import texttable
import select

from time import sleep
from texttable import Texttable, get_color_string, bcolors


class PrinterInfo (threading.Thread):
    
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.table = texttable.Texttable()
        self.info = {}
        self.index = 0
        self.createTable('ESSID                 ','BSSID            ','STATION          ', 'PROBE_REQ', 'AUTH','DEAUTH', 'PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON','TOT_PACK', bcolors.BLUE)
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)
        self.essid = {}
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.stopSniff = False
        self.src = curses.initscr()
        curses.noecho()
        #curses.endwin()
        self.srcHeight = 10
        self.mypad_pos = 0
        
        self.src = curses.newpad(self.srcHeight,300)
        
        self.src.nodelay(1)
        self.src.keypad(True)
        self.src.insstr(0,0, self.table.draw())
        #self.cmd = None
        
    
    #def updateGetch(self):
        ##while (True):
        #self.cmd = self.src.getch()
    
    
    def run(self):
        
        while (not self.stopSniff):
            #self.printInformation()

            self.src.clear()
            self.src.resize(self.srcHeight+100, 300)
            self.src.insstr(0, 0, self.table.draw())
            
            self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
            
            cmd = self.src.getch()
            if cmd == curses.KEY_UP:
            #if  cmd == self.src.keypad(1):
            #if  cmd == ord('s'):
                #print "WEEEEEEEEEEEEEEEE"
                self.mypad_pos += 10
                #self.src.move(mypad_pos,0)
                self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
            if cmd == curses.KEY_DOWN:
            #elif  cmd == ord('w'):
            #elif cmd == self.src.keypad(4):
                self.mypad_pos -= 10
                self.src.refresh(self.mypad_pos, 0, 0, 0, 50, 190)
            elif cmd == ord('q'):
                curses.endwin()
                self.stopSniff = True
            
            #self.src.refresh()
    
    def addInfo(self,i):
        if i[0] != "" and i[0] != None:
            self.essid[(i[1],i[2])] = i[0]
        if (i[1],i[2]) not in self.info:
            self.info[(i[1],i[2])] = i
            self.index += 1
        else:
            if i[0] == "" and (i[1],i[2]) in self.essid and self.essid[(i[1],i[2])] != "":
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
        self.createTable('ESSID                 ','BSSID            ','STATION          ','PROBE_REQ','AUTH','DEAUTH','PWR','HAND_SUCC','HAND_FAIL','CORRUPT','CORR %','DATA','RTS','CTS','ACK','BEACON','TOT_PACK', bcolors.BLUE)
        #self.createTable('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT', bcolors.BLUE)

        for i in self.info:
            self.table.add_rows([self.info[i]],False)
                
        #self.src.addstr(self.table.draw() + "\n")
        
    def createTable(self,essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, tot_pack, color):
        self.table.set_deco(Texttable.HEADER)
        self.table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c"])
        self.table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"])
        #self.table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
        self.table.add_rows([[essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt, corrPercent, data, rts, cts, ack, beacon, tot_pack]])
        #self.src.refresh()
        #print(self.table.draw() + "\n")


    def setStopSniff(self, stopSniff):
        self.stopSniff = stopSniff
