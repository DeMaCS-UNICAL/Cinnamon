import scapy
import scapy_ex
import os,sys, socket
import printerInfo

from scapy.layers.dot11 import Dot11
from scapy.all import *
#from time import sleep


class SniffPackage:
    
    BROADCAST_ADDR = "ff:ff:ff:ff:ff:ff"
    
    def __init__(self, printerInfo):
        self.apPresent = {}

        self.essid = {}
        #channel = {}

        self.packages = []
        self.index = 0

        self.frequence = {}
        self.authent = {}
        self.deauthent = {}
        self.probeRequest = {}
        self.eapHandshakeSuccess = {}
        self.eapHandshakeFailed = {}
        self.corruptedPack = {}

        self.eapRequest = {}
        
        self.rtsList = {}
        self.ctsList = {}
        self.dataList = {}
        self.ackList = {}
        
        self.beaconList = {}
        
        self.numPack = {}
        self.cont = 0
        self.printerInfo = printerInfo


    def createArray(self,macAP, macClient):
        if macAP != None and macClient != None and macClient not in self.apPresent:
        #if macClient not in self.apPresent:
            if macAP not in self.apPresent:
                self.apPresent[macAP] = []
                self.apPresent[macAP].append(macClient)
        
        if (macAP,macClient) not in self.deauthent:
            self.deauthent[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.authent:
            self.authent[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.frequence:
            self.frequence[(macAP,macClient)] = "-"
        if (macAP,macClient) not in self.eapHandshakeSuccess:
            self.eapHandshakeSuccess[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.eapHandshakeFailed:
            self.eapHandshakeFailed[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.corruptedPack:
            self.corruptedPack[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.rtsList:
            self.rtsList[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.ctsList:
            self.ctsList[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.dataList:
            self.dataList[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.numPack:
            self.numPack[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.ackList:
            self.ackList[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.beaconList:
            self.beaconList[(macAP,macClient)] = 0
        
        

    def checkFrequence(self,macAP, macClient,freq):
        if freq != 0 and freq != None:
            if macAP != SniffPackage.BROADCAST_ADDR:
                self.frequence[(macAP,macClient)] = freq

    def printInfo(self,essid,macAP,macClient):
        if macAP != None and macClient != None:
            #print essid
            if (essid,macClient) not in self.probeRequest:
                self.probeRequest[(essid,macClient)] = 0
            
            
            #percentCorr = float(float(self.corruptedPack[(macAP,macClient)])/100)
            percentCorr = 0
            if self.numPack[(macAP,macClient)] != 0:
                percentCorr = int(float(self.corruptedPack[(macAP,macClient)])/float(self.numPack[(macAP,macClient)])*100)
            
            strPercentage = str(percentCorr)+"%"
            
            i = tuple([essid, macAP, macClient, self.probeRequest[(essid,macClient)], self.authent[(macAP,macClient)], self.deauthent[(macAP,macClient)], self.frequence[(macAP,macClient)], self.eapHandshakeSuccess[(macAP,macClient)], self.eapHandshakeFailed[(macAP,macClient)], self.corruptedPack[(macAP,macClient)], strPercentage, self.dataList[(macAP,macClient)], self.rtsList[(macAP,macClient)], self.ctsList[(macAP,macClient)], self.ackList[(macAP,macClient)], self.beaconList[(macAP,macClient)], self.numPack[(macAP,macClient)]])
            self.printerInfo.addInfo(i)
        

    def checkFCS(self,p, from_DS, to_DS):
        #if p.haslayer(Dot11ProbeReq):
        if hasattr(p, 'Flags') and p.Flags is not None:
            if p.Flags & 64 != 0:
                if not from_DS and to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        #print "FIRST: ",p.addr1, " ", p.addr2
                        if p.addr1 != None and p.addr2 != None:
                            self.createArray(p.addr1,p.addr2)
                            self.corruptedPack[(p.addr1,p.addr2)] += 1
                            self.numPack[(p.addr1,p.addr2)] += 1
                            if hasattr(p, 'info'):
                                self.printInfo(p.info,p.addr1,p.addr2)
                            else:
                                self.checkEssid(p.addr1, p.addr2)
                                #if p.addr1 in self.essid:
                                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                                #else:
                                    #self.printInfo("",p.addr1,p.addr2)
                elif from_DS and not to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        #print "SECOND: ----------",p.addr2, " ", p.addr1
                        if p.addr1 != None and p.addr2 != None:
                            self.createArray(p.addr2,p.addr1)
                            self.corruptedPack[(p.addr2,p.addr1)] += 1
                            self.numPack[(p.addr2,p.addr1)] += 1
                            if hasattr(p, 'info'):
                                if p.info != "":
                                    self.printInfo(p.info,p.addr2,p.addr1)
                                else:
                                    self.checkEssid(p.addr2, p.addr1)
                            else:
                                self.checkEssid(p.addr2, p.addr1)
                                #if p.addr2 in self.essid:
                                    #self.printInfo(self.essid[p.addr2],p.addr2,p.addr1)
                                #else:
                                    #self.printInfo("",p.addr2,p.addr1)
                elif not from_DS and not to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        #print "THIRD: ----------",p.addr1, " ", p.addr2
                        if p.addr1 != None and p.addr2 != None:
                            if p.addr1 in self.apPresent:
                                macAP = p.addr1
                                macClient = p.addr2
                            else:
                                macAP = p.addr2
                                macClient = p.addr1
                            self.createArray(macAP, macClient)
                            self.corruptedPack[(macAP, macClient)] += 1
                            self.numPack[(macAP, macClient)] += 1
                            if hasattr(p, 'info'):
                                if p.info != "":
                                    self.printInfo(p.info,macAP, macClient)
                                else:
                                    self.checkEssid(macAP, macClient)
                            else:
                                self.checkEssid(macAP, macClient)
                                #if p.addr2 in self.essid:
                                    #self.printInfo(self.essid[p.addr2],p.addr2,p.addr1)
                                #else:
                                    #self.printInfo("",p.addr2,p.addr1)
                return True
            
            else:
                return False
            #else: return False


    def checkEssid(self, macAP, macClient):
        if macAP in self.essid:
            self.printInfo(self.essid[macAP], macAP, macClient)
        else:
            self.printInfo("-", macAP, macClient)

    def sniffmgmt(self,p):
        #p.show()
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #ls(p)
        #PR = p.present & 0x7
        #flag = PR & 0x1 != 0
        #print flag
        
        #self.packages.append(p)
        #Dot11.enable_FCS(True)
        
        from_DS = None
        to_DS = None
        
        if hasattr(p, 'FCfield') and p.FCfield is not None:
            DS = p.FCfield & 0x3
            to_DS = DS & 0x1 != 0
            from_DS = DS & 0x2 != 0
        
        
        isCorrupted = self.checkFCS(p, from_DS, to_DS)
        if isCorrupted:
            return
        #isCorrupted = False
        elif not isCorrupted:
            activeAp = 0
            if (not from_DS and to_DS) or (not from_DS and not to_DS):
                #print self.apPresent
                if p.addr1 not in self.apPresent and p.addr2 != None:
                    #print "FIRST ", p.addr1, " ", p.addr2
                    self.createArray(p.addr1,p.addr2)
                    self.numPack[p.addr1,p.addr2] += 1
                #self.checkEssid(p.addr1, p.addr2)
            elif from_DS and not to_DS:
                #print "SECOND ", p.addr3, " ", p.addr1
                if p.addr2 in apPresent and p.addr1 in apPresent[p.addr2]:
                    
                self.createArray(p.addr3,p.addr1)
                self.numPack[p.addr3,p.addr1] += 1   
                #self.checkEssid(p.addr3, p.addr1)
            #p.show()
            
            if p.haslayer(Dot11) and hasattr(p, 'info'):
                ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
                activeAp = 1
                #print "------------------------------------ ", ssid
                if p.addr3 not in self.apPresent:
                    self.apPresent[p.addr3] = []
                #if p.addr3 != SniffPackage.BROADCAST_ADDR:
                    #print "+++++++++++++++++++++++++++++++++++ ", ssid, " ", p.addr3
                self.essid[p.addr3] = ssid
                self.createArray(p.addr3, p.addr2)
                self.checkEssid(p.addr3, p.addr2)
                #self.printInfo(self.essid[p.addr3], p.addr3, p.addr2)
            
            
            if from_DS and not to_DS and p.addr3 != SniffPackage.BROADCAST_ADDR and p.addr1 != SniffPackage.BROADCAST_ADDR:
                key = "%s" % (p.addr3)
                self.createArray(key, p.addr1)
                self.checkEssid(key, p.addr1)
                #self.checkFrequence(key,p.addr1,p.dBm_AntSignal)
                #if key in self.essid:
                    #self.printInfo(self.essid[key],key,p.addr1)
                #else:
                    #self.printInfo("<hidden>",key,p.addr1)
                #return

            #elif activeAp == 0:
            elif not from_DS and to_DS and p.addr2 != SniffPackage.BROADCAST_ADDR:
                key = "%s" % (p.addr1)
                if key not in self.apPresent:
                    self.apPresent[p.addr3] = []
                if key in self.apPresent:
                    if p.addr2 not in self.apPresent[key]:
                        self.apPresent[key].append(p.addr2)
                    self.createArray(key, p.addr2)
                    self.checkFrequence(key,p.addr2,p.dBm_AntSignal)
                    self.checkEssid(key, p.addr2)
                    #if key in self.essid:
                        #self.printInfo(self.essid[key],key,p.addr2)
                    #else:
                        #self.printInfo("<hidden>",key,p.addr2)
            
            
            if p.haslayer(EAP):
                #if p["EAP":].code == 1: # --------------------> REQUEST
                    #self.eapRequest[(p.addr2,p.addr1)] = 1
                #elif p["EAP":].code == 2: # --------------------------> RESPONSE
                    #if (p.addr1,p.addr2) in self.eapRequest and self.eapRequest[(p.addr1,p.addr2)] == 1:
                        #self.eapRequest[(p.addr1,p.addr2)] = 2
                if p["EAP":].code == 3: # -----------------------> SUCCESS
                    #p.show()
                    if (p.addr2,p.addr1) not in self.eapHandshakeSuccess:
                        self.createArray(p.addr2, p.addr1)
                    #self.eapRequest[(p.addr2,p.addr1)] = 0
                    self.eapHandshakeSuccess[(p.addr2,p.addr1)] += 1
                    self.checkEssid(p.addr2, p.addr1)
                    #self.printInfo(self.essid[p.addr2],p.addr2,p.addr1)
                    return
                elif p["EAP":] == 4: # --------------------> FAILED
                    if (p.addr2,p.addr1) in self.eapRequest:
                        self.eapHandshakeSuccess[(p.addr2,p.addr1)] = 0
                        #self.eapRequest[(p.addr2,p.addr1)] = 0
                    self.eapHandshakeFailed[(p.addr2,p.addr1)] += 1
                    self.checkEssid(p.addr2, p.addr1)
                    return
            
            if hasattr(p, 'type') and p.type == 2 and hasattr(p, 'subtype') and p.subtype == 8:   #BEACON
                #p.show()
                #self.cont += 1
                #print p.addr1, " ", p.addr2, " ", p.addr3, " ----> ", from_DS, " ", to_DS
                if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    self.createArray(p.addr1,p.addr2)
                    self.beaconList[p.addr1,p.addr2] += 1
                    self.checkEssid(p.addr1, p.addr2)
                elif from_DS and not to_DS:
                    self.createArray(p.addr2,p.addr1)
                    self.beaconList[p.addr2,p.addr1] += 1   
                    self.checkEssid(p.addr2, p.addr1)
                return
            if hasattr(p, 'type') and p.type == 2 and hasattr(p, 'subtype') and p.subtype == 0:   #DATA
                #p.show()
                if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    self.createArray(p.addr1,p.addr2)
                    self.dataList[p.addr1,p.addr2] += 1
                    self.checkEssid(p.addr1, p.addr2)
                elif from_DS and not to_DS:
                    self.createArray(p.addr3,p.addr1)
                    self.dataList[p.addr3,p.addr1] += 1   
                    self.checkEssid(p.addr3, p.addr1)
                return
                    
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 11:   #RTS
                if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    if p.addr1 in self.apPresent:
                        macAP = p.addr1
                        macClient = p.addr2
                    else:
                        macAP = p.addr2
                        macClient = p.addr1
                    self.createArray(macAP, macClient)
                    self.rtsList[macAP, macClient] += 1   
                    self.checkEssid(macAP, macClient)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                elif from_DS and not to_DS:
                    self.createArray(p.addr3,p.addr1)
                    self.rtsList[p.addr3,p.addr1] += 1   
                    self.checkEssid(p.addr3, p.addr1)
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 12:   #CTS
                if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    self.createArray(p.addr1,p.addr2)
                    self.ctsList[p.addr1,p.addr2] += 1   
                    self.checkEssid(p.addr1, p.addr2)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                elif from_DS and not to_DS:
                    self.createArray(p.addr3,p.addr1)
                    self.ctsList[p.addr3,p.addr1] += 1   
                    self.checkEssid(p.addr3, p.addr1)
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 13:   #ACK
                #p.show()
                if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    self.createArray(p.addr1,p.addr2)
                    self.ackList[p.addr1,p.addr2] += 1   
                    self.checkEssid(p.addr1, p.addr2)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                elif from_DS and not to_DS:
                    self.createArray(p.addr3,p.addr1)
                    self.ackList[p.addr3,p.addr1] += 1   
                    self.checkEssid(p.addr3, p.addr1)
                
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
                    
            
            
            if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 11:   #AUTH
                #p.show()
                if p.addr1 in self.apPresent:
                    macAP = p.addr1
                    macClient = p.addr2
                    #print "IIIIIIIIN -------------------------------------------------------------------- ", macAP, " ", macClient
                else:
                    macAP = p.addr2
                    macClient = p.addr1
                    #print "NOOOOOOOOOOOOT -------------------------------------------------------------------- ", macAP, " ", macClient
                    
                self.createArray(macAP, macClient)
                #if p.addr1 in apPresent:
                    #if p.addr2 not in apPresent[p.addr1]:
                        #apPresent[p.addr1].append(p.addr2);
                
                self.authent[macAP, macClient] += 1 
                self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                self.checkEssid(macAP, macClient)
                #printInfo(essid[p.addr1],p.addr1,p.addr2)
                return
                #return
                    
            if hasattr(p, 'type') and hasattr(p, 'subtype') and p.type == 0 and p.subtype == 12:   #DEAUTH
                #p.show()
                if p.addr1 in self.apPresent:
                    macAP = p.addr1
                    macClient = p.addr2
                else:
                    macAP = p.addr2
                    macClient = p.addr1
                self.createArray(macAP, macClient)
                if macAP in self.apPresent:
                    if macClient in self.apPresent[macAP]:
                        self.apPresent[macAP].remove(macClient);
                        
                    self.deauthent[macAP, macClient] += 1
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                    self.checkEssid(macAP, macClient)
                return
                    
            if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 4:   #PROBE_REQ
                self.createArray(p.addr1,p.addr2)
                if (p.info,p.addr2) not in self.probeRequest:
                    self.probeRequest[(p.info,p.addr2)] = 0
                self.probeRequest[(p.info,p.addr2)] += 1
                self.checkFrequence(p.addr1,p.addr2,p.dBm_AntSignal)
                
                self.checkEssid(p.addr1, p.addr2)
                
                #self.printInfo(p.info,p.addr1,p.addr2)
                return
            
            #if activeAp == 1:
            #if from_DS and not to_DS and p.addr3 != SniffPackage.BROADCAST_ADDR and p.addr1 != SniffPackage.BROADCAST_ADDR:
                #key = "%s" % (p.addr3)
                #self.createArray(key, p.addr1)
                ##self.checkFrequence(key,p.addr1,p.dBm_AntSignal)
                #if key in self.essid:
                    #self.printInfo(self.essid[key],key,p.addr1)
                #else:
                    #self.printInfo("<hidden>",key,p.addr1)
                #return

            ##elif activeAp == 0:
            #if not from_DS and to_DS and p.addr2 != SniffPackage.BROADCAST_ADDR:
                #key = "%s" % (p.addr1)
                #if key not in self.apPresent:
                    #self.apPresent[p.addr3] = []
                #if key in self.apPresent:
                    #if p.addr2 not in self.apPresent[key]:
                        #self.apPresent[key].append(p.addr2)
                    #self.createArray(key, p.addr2)
                    ##self.checkFrequence(key,p.addr2,p.dBm_AntSignal)
                    #if key in self.essid:
                        #self.printInfo(self.essid[key],key,p.addr2)
                    #else:
                        #self.printInfo("<hidden>",key,p.addr2)
                    #return

        #self.printInfo(p.info,p.addr1,p.addr2)


    def takePack(self):
        return self.packages

    def printClientConnect(self):
        for key in self.apPresent:
            print "NUM CLIENT CONNECT IN AP: "+ key + " ", len(self.apPresent[key])
            for c in self.apPresent[key]:
                print c

    def takeCont(self):
        return self.cont

#if __name__ == "__main__":

    #for line in sys.stdin:
        #sys.stdout.write(line)
