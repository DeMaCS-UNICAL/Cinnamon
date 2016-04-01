import scapy
import scapy_ex
import os
import texttable

from scapy.layers.dot11 import Dot11
from scapy.all import *
from texttable import Texttable, get_color_string, bcolors
from time import sleep

apPresent = {}

essid = {}
#channel = {}

frequence = {}
authent = {}
deauthent = {}
probeRequest = {}
eapHandshakeSuccess = {}
eapHandshakeFailed = {}
corruptedPack = {}

eapRequest = {}

table = texttable.Texttable()
color = bcolors.BLUE

BROADCAST_ADDR = "ff:ff:ff:ff:ff:ff"

def createTable(essid, bssid, station, probe_req, auth, deauth, freq, hand_succ, hand_fail, corrupt):
    table.set_cols_align(["l", "r", "c", "c","c", "c", "c", "c", "c", "c"])
    table.set_cols_valign(["t", "b", "m", "b", "b", "b", "b", "b", "b", "b"])
    table.add_rows([ [get_color_string(color, essid), get_color_string(color, bssid), get_color_string(color, station), get_color_string(color, probe_req), get_color_string(color, auth), get_color_string(color, deauth), get_color_string(color, freq), get_color_string(color, hand_succ),get_color_string(color, hand_fail), get_color_string(color, corrupt)]])
    
    print(table.draw() + "\n")


def createArray(macAP, macClient):
    if (macAP,macClient) not in deauthent:
        deauthent[(macAP,macClient)] = 0
    if (macAP,macClient) not in authent:
        authent[(macAP,macClient)] = 0
    if (macAP,macClient) not in frequence:
        frequence[(macAP,macClient)] = "-"
    if (macAP,macClient) not in eapHandshakeSuccess:
        eapHandshakeSuccess[(macAP,macClient)] = 0
    if (macAP,macClient) not in eapHandshakeFailed:
        eapHandshakeFailed[(macAP,macClient)] = 0
    if (macAP,macClient) not in corruptedPack:
        corruptedPack[(macAP,macClient)] = 0
    


def checkFrequence(macAP, macClient,freq):
    if freq != 0 and freq != None:
        if macAP != BROADCAST_ADDR:
            frequence[(macAP,macClient)] = freq


def printInfo(essid,macAP,macClient):
    if (essid,macClient) not in probeRequest:
        probeRequest[(essid,macClient)] = 0
        
    table.add_rows([[essid, macAP, macClient, probeRequest[(essid,macClient)], authent[(macAP,macClient)], deauthent[(macAP,macClient)], frequence[(macAP,macClient)], eapHandshakeSuccess[(macAP,macClient)], eapHandshakeFailed[(macAP,macClient)], corruptedPack[(macAP,macClient)]]], False)
    #print "{0:20}\t{1:30}\t{2:20}\t{3:5}\t{4:5}\t{5:5}\t{6:5}\t{7:5}\t{8:5}\t{9:5}".format(essid, macAP, macClient, probeRequest[(essid,macClient)], authent[(macAP,macClient)], deauthent[(macAP,macClient)], frequence[(macAP,macClient)], eapHandshakeSuccess[(macAP,macClient)], eapHandshakeFailed[(macAP,macClient)], corruptedPack[(macAP,macClient)])
    clear = lambda: os.system('clear') * 100
    clear()
    print(table.draw() + "\n") 
    sleep(0.05)

def checkFCS(p, from_DS, to_DS):
    if p.Flags is not None:
        if p.Flags & 64 != 0:
            if not from_DS and to_DS:
                if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                    if p.addr1 != None and p.addr2 != None:
                        createArray(p.addr1,p.addr2)
                        corruptedPack[(p.addr1,p.addr2)] +=1
                        if hasattr(p, 'info'):
                            printInfo(p.info,p.addr1,p.addr2)
                        else:
                            printInfo("",p.addr1,p.addr2)
            else:
                if hasattr(p, 'addr3') and hasattr(p, 'addr2'):
                    if p.addr3 != None and p.addr2 != None:
                        createArray(p.addr2,p.addr3)
                        corruptedPack[(p.addr2,p.addr3)] +=1
                        if hasattr(p, 'info'):
                            printInfo(p.info,p.addr2,p.addr3)
                        
                        else:
                            printInfo("",p.addr2,p.addr3)
            
            return True
        
        else:
            return False


def sniffmgmt(p):
    #Dot11.enable_FCS(True)

    from_DS = None
    to_DS = None
    
    if hasattr(p, 'FCfield') and p.FCfield is not None:
        DS = p.FCfield & 0x3
        to_DS = DS & 0x1 != 0
        from_DS = DS & 0x2 != 0
        
    isCorrupted = checkFCS(p, from_DS, to_DS)
    
    if not isCorrupted:
        activeAp = 0
        #p.show()
        
        if p.haslayer(Dot11) and hasattr(p, 'info'):
            ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
            activeAp = 1
            if p.addr3 not in apPresent and p.addr3 != BROADCAST_ADDR:
                apPresent[p.addr3] = []
                essid[p.addr3] = ssid
        
        if p.haslayer("EAP"):
            if p["EAP":].code == 1: # --------------------> REQUEST
                eapRequest[(p.addr2,p.addr1)] = 1
            elif p["EAP":].code == 2: # --------------------------> RESPONSE
                if (p.addr1,p.addr2) in eapRequest and eapRequest[(p.addr1,p.addr2)] == 1:
                    eapRequest[(p.addr1,p.addr2)] = 2
            elif p["EAP":].code == 3: # -----------------------> SUCCESS
                if (p.addr2,p.addr1) in eapRequest and eapRequest[(p.addr2,p.addr1)] == 2:
                    eapRequest[(p.addr2,p.addr1)] = 0
                    eapHandshakeSuccess[(p.addr2,p.addr1)] += 1
                    printInfo(essid[p.addr2],p.addr2,p.addr1)
                    return
            elif p["EAP":] == 4: # --------------------> FAILED
                if (p.addr2,p.addr1) in eapRequest:
                    eapHandshakeSuccess[(p.addr2,p.addr1)] = 0
                    eapRequest[(p.addr2,p.addr1)] = 0
                
                eapHandshakeFailed[(p.addr2,p.addr1)] += 1
        
                    
        if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 11:   #AUTH
            createArray(p.addr1,p.addr2)
            #if p.addr1 in apPresent:
                #if p.addr2 not in apPresent[p.addr1]:
                    #apPresent[p.addr1].append(p.addr2);
            
            authent[p.addr1,p.addr2] += 1 
            checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
            #printInfo(essid[p.addr1],p.addr1,p.addr2)
            #return
                
        if hasattr(p, 'type') and hasattr(p, 'subtype') and p.type == 0 and p.subtype == 12:   #DEAUTH
            createArray(p.addr1, p.addr2)
            if p.addr1 in apPresent:
                if p.addr2 in apPresent[p.addr1]:
                    apPresent[p.addr1].remove(p.addr2);
                    
                deauthent[p.addr1,p.addr2] += 1
                checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
                printInfo(essid[p.addr1],p.addr1,p.addr2)
                return
                
        if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 4:   #PROBE_REQ
            createArray(p.addr1,p.addr2)
            if (p.info,p.addr2) not in probeRequest:
                probeRequest[(p.info,p.addr2)] = 0
            probeRequest[(p.info,p.addr2)] += 1
            checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
            
            printInfo(p.info,p.addr1,p.addr2)
            return
        
        if activeAp == 1:
            if from_DS and not to_DS and p.addr3 != BROADCAST_ADDR and p.addr1 != BROADCAST_ADDR:
                key = "%s" % (p.addr3)
                createArray(key, p.addr1)
                checkFrequence(key,p.addr1,p.dBm_AntSignal)
                            
                printInfo(essid[key],key,p.addr1)
                return

        elif activeAp == 0:
            if not from_DS and to_DS and p.addr2 != BROADCAST_ADDR:
                key = "%s" % (p.addr1)
                if key in apPresent:
                    if p.addr2 not in apPresent[key]:
                        apPresent[key].append(p.addr2)
                    createArray(key, p.addr2)
                    checkFrequence(key,p.addr2,p.dBm_AntSignal)
                    
                    printInfo(essid[key],key,p.addr2)
                    return



def printClientConnect():
    for key in apPresent:
        print "NUM CLIENT CONNECT IN AP: "+ key + " ", len(apPresent[key])
        for c in apPresent[key]:
            print c
