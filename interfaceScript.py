import scapy
import scapy_ex

from scapy.layers.dot11 import Dot11

apPresent = {}

essid = {}
#channel = {}

frequence = {}
authent = {}
deauthent = {}
probeRequest = {}

def createArray(macAP, macClient):
    if (macAP,macClient) not in deauthent:
        deauthent[(macAP,macClient)] = 0
    if (macAP,macClient) not in authent:
        authent[(macAP,macClient)] = 0
    if (macAP,macClient) not in probeRequest:
        probeRequest[(macAP,macClient)] = 0
    if (macAP,macClient) not in frequence:
        frequence[(macAP,macClient)] = "-"


def checkFrequence(macAP, macClient,freq):
    if freq != 0 and freq != None:
        if macAP != "ff:ff:ff:ff:ff:ff":
            frequence[(macAP,macClient)] = freq
        #p.show()

    
def sniffmgmt(p):
    
    #if p.dBm_AntSignal != 0 and p.dBm_AntSignal != None:
        #p.show()

    if p.FCfield is not None:
        DS = p.FCfield & 0x3
        to_DS = DS & 0x1 != 0
        from_DS = DS & 0x2 != 0
    
    activeAp = 0
    #auth = 0
    #deauth = 0
    #probeReq = 0
    
    #print p.present.Channel
    #freq = -(256-ord(p.notdecoded[-4:-3])) #--> Signal
    
    if p.haslayer(Dot11) and hasattr(p, 'info'):
        ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
        #if p.haslayer(Dot11Elt):
            #if p[Dot11Elt:3].len == 1:
                #chan = ord(p[Dot11Elt:3].info)
        #if ssid == "Martensson-WIFI":
        activeAp = 1
        if p.addr3 not in apPresent and p.addr3 != "ff:ff:ff:ff:ff:ff":
            apPresent[p.addr3] = []
            essid[p.addr3] = ssid
    
    if p.type == 0 and p.subtype == 11:   #AUTH
        #auth = 1
        createArray(p.addr1,p.addr2)
        #if p.addr1 in apPresent:
            #if p.addr2 not in apPresent[p.addr1]:
                #apPresent[p.addr1].append(p.addr2);
        
        authent[p.addr1,p.addr2] += 1 
        checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
        return
            
    if p.type == 0 and p.subtype == 12:   #DEAUTH
        #deauth = 1
        createArray(p.addr1, p.addr2)
        if p.addr1 in apPresent:
            if p.addr2 in apPresent[p.addr1]:
                apPresent[p.addr1].remove(p.addr2);
                
            deauthent[p.addr1,p.addr2] += 1
            checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
            return
            
    if p.type == 0 and p.subtype == 4:   #PROBE_REQ
        if p.addr1 == "ff:ff:ff:ff:ff:ff":
            createArray(p.addr1,p.addr2)
            probeRequest[(p.addr1,p.addr2)] += 1
            checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
            
            print "{0:20}\t{1:30}\t{2:20}\t{3:5}\t{4:10}\t{5:5}\t{6:2}".format("-", p.addr1, p.addr2, probeRequest[(p.addr1,p.addr2)], authent[(p.addr1,p.addr2)], deauthent[(p.addr1,p.addr2)], frequence[(p.addr1,p.addr2)])
            return
        #else:
            #probeReq = 1
    
    if activeAp == 1:
        if not from_DS and not to_DS and p.addr3 != "ff:ff:ff:ff:ff:ff" and p.addr1 != "ff:ff:ff:ff:ff:ff":
            key = "%s" % (p.addr3)
            createArray(key, p.addr1)
            #print p.addr1, " ", p.addr2, " ", p.addr3
            #if key not in apPresent:
                #apPresent[key] = []
            #if ssid not in essid[key]:
                #essid[key] = ssid
                #channel[key] = chan
            checkFrequence(key,p.addr1,p.dBm_AntSignal)
            
            print "{0:20}\t{1:30}\t{2:20}\t{3:5}\t{4:10}\t{5:5}\t{6:2}".format(essid[key], key, p.addr1, probeRequest[(key,p.addr1)], authent[(key, p.addr1)], deauthent[(key, p.addr1)], frequence[(key, p.addr1)])

    elif activeAp == 0:
        if not from_DS and to_DS and p.addr2 != "ff:ff:ff:ff:ff:ff":
            key = "%s" % (p.addr1)
            if key in apPresent:
                #apPresent[key] = []
                if p.addr2 not in apPresent[key]:
                    apPresent[key].append(p.addr2)
                createArray(key, p.addr2)
                checkFrequence(key,p.addr2,p.dBm_AntSignal)
                
                print "{0:20}\t{1:30}\t{2:20}\t{3:5}\t{4:10}\t{5:5}\t{6:2}".format(essid[key], key, p.addr2, probeRequest[(key,p.addr2)], authent[(key, p.addr2)], deauthent[(key, p.addr2)], frequence[(key, p.addr2)]) 
        





def printClientConnect():
    for key in apPresent:
        print "NUM CLIENT CONNECT IN AP: "+ key + " ", len(apPresent[key])
        for c in apPresent[key]:
            print c
