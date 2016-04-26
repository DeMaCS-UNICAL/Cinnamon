import scapy
import scapy_ex
import os,sys, socket
import printerInfo

import enum
from enum import Enum

from scapy.layers.dot11 import Dot11
from scapy.all import *
#from time import sleep


class Message(Enum):
    AUTH = "0"
    DEAUTH = "1"

    PROBE_REQ = "2"
    
    HAND_SUCC = "3"
    HAND_FAIL = "4"
    
    CORR_PACK = "5"
    RTS = "6"

    CTS = "7"
    ACK = "8"

    DATA = "9"
    BEACON = "10"
    NUM_PACK = "11"


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
        self.authentAP = {}
        self.authentClient = {}
        
        self.deauthent = {}
        self.deauthentAP = {}
        self.deauthentClient = {}
        
        self.probeRequest = {}
        self.probeRequestAP = {}
        self.probeRequestClient = {}
        
        self.eapHandshakeSuccess = {}
        self.eapHandshakeSuccessAP = {}
        self.eapHandshakeSuccessClient = {}
        
        self.eapHandshakeFailed = {}
        self.eapHandshakeFailedAP = {}
        self.eapHandshakeFailedClient = {}
        
        self.corruptedPack = {}
        self.corruptedPackAP = {}
        self.corruptedPackClient = {}

        self.eapRequest = {}
        
        self.rtsList = {}
        self.rtsListAP = {}
        self.rtsListClient = {}
        
        self.ctsList = {}
        self.ctsListAP = {}
        self.ctsListClient = {}
        
        self.dataList = {}
        self.dataListAP = {}
        self.dataListClient = {}
        
        self.ackList = {}
        self.ackListAP = {}
        self.ackListClient = {}
        
        self.beaconList = {}
        self.beaconAP = {}
        self.beaconClient = {}
        
        self.numPack = {}
        self.numPackAP = {}
        self.numPackClient = {}
        
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
        if macClient not in self.ackList:
            self.ackList[macClient] = 0
        
    
    def createArrayAP(self, macAP):
        if macAP not in self.apPresent:
            self.apPresent[macAP] = []
                
        if macAP not in self.beaconAP:
            self.beaconAP[macAP] = 0
        if macAP not in self.numPackAP:
            self.numPackAP[macAP] = 0
        if macAP not in self.authentAP:
            self.authentAP[macAP] = 0
        if macAP not in self.deauthentAP:
            self.deauthentAP[macAP] = 0
        if macAP not in self.probeRequestAP:
            self.probeRequestAP[macAP] = 0
        if macAP not in self.eapHandshakeSuccessAP:
            self.eapHandshakeSuccessAP[macAP] = 0
        if macAP not in self.eapHandshakeFailedAP:
            self.eapHandshakeFailedAP[macAP] = 0
        if macAP not in self.corruptedPackAP:
            self.corruptedPackAP[macAP] = 0
        if macAP not in self.rtsListAP:
            self.rtsListAP[macAP] = 0
        if macAP not in self.ctsListAP:
            self.ctsListAP[macAP] = 0
        if macAP not in self.dataListAP:
            self.dataListAP[macAP] = 0
        if macAP not in self.ackListAP:
            self.ackListAP[macAP] = 0
            
    def createArrayClient(self, macClient):
        if macClient not in self.beaconClient:
            self.beaconClient[macClient] = 0
        if macClient not in self.numPackClient:
            self.numPackClient[macClient] = 0
        if macClient not in self.authentClient:
            self.authentClient[macClient] = 0
        if macClient not in self.deauthentClient:
            self.deauthentClient[macClient] = 0
        if macClient not in self.probeRequestClient:
            self.probeRequestClient[macClient] = 0
        if macClient not in self.eapHandshakeSuccessClient:
            self.eapHandshakeSuccessClient[macClient] = 0
        if macClient not in self.eapHandshakeFailedClient:
            self.eapHandshakeFailedClient[macClient] = 0
        if macClient not in self.corruptedPackClient:
            self.corruptedPackClient[macClient] = 0
        if macClient not in self.rtsListClient:
            self.rtsListClient[macClient] = 0
        if macClient not in self.ctsListClient:
            self.ctsListClient[macClient] = 0
        if macClient not in self.dataListClient:
            self.dataListClient[macClient] = 0
        if macClient not in self.ackListClient:
            self.ackListClient[macClient] = 0
    
    

    def checkFrequence(self,macAP, macClient,freq):
        if freq != 0 and freq != None:
            if macAP != SniffPackage.BROADCAST_ADDR:
                self.frequence[(macAP,macClient)] = freq

    def printInfo(self,essid,macAP,macClient):
        if macAP != None and macClient != None:
            if (essid,macClient) not in self.probeRequest:
                self.probeRequest[(essid,macClient)] = 0
            
            
            #percentCorr = float(float(self.corruptedPack[(macAP,macClient)])/100)
            percentCorr = 0
            if self.numPack[(macAP,macClient)] != 0:
                percentCorr = int(float(self.corruptedPack[(macAP,macClient)])/float(self.numPack[(macAP,macClient)])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authent[(macAP,macClient)], self.deauthent[(macAP,macClient)], self.frequence[(macAP,macClient)], self.eapHandshakeSuccess[(macAP,macClient)], self.eapHandshakeFailed[(macAP,macClient)], self.corruptedPack[(macAP,macClient)], strPercentage, self.dataList[(macAP,macClient)], self.rtsList[(macAP,macClient)], self.ctsList[(macAP,macClient)], self.ackList[(macAP, macClient)], self.beaconList[(macAP,macClient)],  self.probeRequest[(essid,macClient)], self.numPack[(macAP,macClient)]])
            self.printerInfo.addInfo(i)
    
    
    def printInfoAP(self, essid, macAP, macClient):
        if macAP != None and macAP != SniffPackage.BROADCAST_ADDR and macClient != None:
            if (macAP) not in self.probeRequestAP:
                self.probeRequestAP[macAP] = 0
            
            
            #percentCorr = float(float(self.corruptedPack[(macAP,macClient)])/100)
            percentCorr = 0
            if self.numPackAP[macAP] != 0:
                percentCorr = int(float(self.corruptedPackAP[macAP])/float(self.numPackAP[macAP])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authentAP[macAP], self.deauthentAP[macAP], "-", self.eapHandshakeSuccessAP[macAP], self.eapHandshakeFailedAP[macAP], self.corruptedPackAP[macAP], strPercentage, self.dataListAP[macAP], self.rtsListAP[macAP], self.ctsListAP[macAP], self.ackListAP[macAP], self.beaconAP[macAP],  self.probeRequestAP[macAP], self.numPackAP[macAP]])
            self.printerInfo.addInfoAP(i)
            
    def printInfoClient(self, essid, macAP, macClient):
        if macAP != None and macClient != None:
            if (macClient) not in self.probeRequestClient:
                self.probeRequestClient[macClient] = 0
            
            
            percentCorr = 0
            if self.numPackClient[macClient] != 0:
                percentCorr = int(float(self.corruptedPackClient[macClient])/float(self.numPackClient[macClient])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authentClient[macClient], self.deauthentClient[macClient], "-", self.eapHandshakeSuccessClient[macClient], self.eapHandshakeFailedClient[macClient], self.corruptedPackClient[macClient], strPercentage, self.dataListClient[macClient], self.rtsListClient[macClient], self.ctsListClient[macClient], self.ackListClient[macClient], self.beaconClient[macClient],  self.probeRequestClient[macClient], self.numPackClient[macClient]])
            self.printerInfo.addInfoClient(i)
    
    
    def createArrayForCorruptPack(self, essid, macAP, macClient, hasInfo):
        self.createArray(macAP, macClient)
        #self.corruptedPack[(macAP, macClient)] += 1
        #self.numPack[(macAP, macClient)] += 1
        
        self.createArrayAndUpdateInfo(macAP, macClient, Message.CORR_PACK)
        #self.createArrayAndUpdateInfo(macAP, macClient, Message.NUM_PACK)
        
        if hasInfo:
            self.printInfo(essid,macAP, macClient)
            self.printInfoAP(essid, macAP, macClient)
            self.printInfoClient(essid, macAP, macClient)
        else:
            self.checkEssid(macAP, macClient)
            self.checkEssidAP(macAP, macClient)
            self.checkEssidClient(macAP, macClient)
    

    def checkFCS(self,p, from_DS, to_DS):
        #if p.haslayer(Dot11ProbeReq):
        if hasattr(p, 'Flags') and p.Flags is not None:
            if p.Flags & 64 != 0:
                if not from_DS and to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        if p.addr1 != None and p.addr2 != None:
                            if hasattr(p, 'info'):
                                self.createArrayForCorruptPack(p.info, p.addr1, p.addr2, True)
                            else:
                                self.createArrayForCorruptPack("", p.addr1, p.addr2, False)
                elif from_DS and not to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        if p.addr1 != None and p.addr2 != None:
                            if hasattr(p, 'info') and p.info != "":
                                self.createArrayForCorruptPack(p.info, p.addr2, p.addr1, True)
                                    #self.printInfo(p.info,p.addr2,p.addr1)
                            else:
                                self.createArrayForCorruptPack("", p.addr2, p.addr1, False)
                elif not from_DS and not to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        if p.addr3 != None and p.addr2 != None:
                            if p.addr3 != p.addr2:
                                macAP = p.addr3
                                macClient = p.addr2
                            else:
                                macAP = p.addr3
                                macClient = None
                            if hasattr(p, 'info') and p.info != "":
                                self.createArrayForCorruptPack(p.info, macAP, macClient, True)
                            else:
                                self.createArrayForCorruptPack("", macAP, macClient, False)
                return True
            
            else:
                return False


    def checkEssid(self, macAP, macClient):
        if macAP in self.essid:
            self.printInfo(self.essid[macAP], macAP, macClient)
        else:
            self.printInfo("-", macAP, macClient)
    def checkEssidAP(self, macAP, macClient):
        if macAP in self.essid:
            self.printInfoAP(self.essid[macAP], macAP, macClient)
        else:
            self.printInfoAP("-", macAP, macClient)
    def checkEssidClient(self, macAP, macClient):
        if macAP in self.essid:
            self.printInfoClient(self.essid[macAP], macAP, macClient)
        else:
            self.printInfoClient("-", macAP, macClient)

    
    def createArrayAndUpdateInfo(self, macAP, macClient, message):
        self.createArray(macAP, macClient)
        self.createArrayAP(macAP)
        self.createArrayClient(macClient)

        if message == Message.AUTH:
            self.authent[(macAP, macClient)] += 1
            self.authentAP[macAP] += 1
            self.authentClient[macClient] += 1
        elif message == Message.DEAUTH:
            self.deauthent[(macAP, macClient)] += 1
            self.deauthentAP[macAP] += 1
            self.deauthentClient[macClient] += 1
        elif message == Message.PROBE_REQ:
            #self.probeRequest[(macAP, macClient)] += 1
            self.probeRequestAP[macAP] += 1
            self.probeRequestClient[macClient] += 1
        elif message == Message.HAND_SUCC:
            self.eapHandshakeSuccess[(macAP, macClient)] += 1
            self.eapHandshakeSuccessAP[macAP] += 1
            self.eapHandshakeSuccessClient[macClient] += 1
        elif message == Message.HAND_FAIL:
            self.eapHandshakeFailed[(macAP, macClient)] += 1
            self.eapHandshakeFailedAP[macAP] += 1
            self.eapHandshakeFailedClient[macClient] += 1
        elif message == Message.CORR_PACK:
            self.corruptedPack[(macAP, macClient)] += 1
            self.corruptedPackAP[macAP] += 1
            self.corruptedPackClient[macClient] += 1
        elif message == Message.RTS:
            self.rtsList[(macAP, macClient)] += 1
            self.rtsListAP[macAP] += 1
            self.rtsListClient[macClient] += 1
        elif message == Message.CTS:
            self.ctsList[(macAP, macClient)] += 1
            self.ctsListAP[macAP] += 1
            self.ctsListClient[macClient] += 1
        elif message == Message.ACK:
            self.ackList[(macAP, macClient)] += 1
            self.ackListAP[macAP] += 1
            self.ackListClient[macClient] += 1
        elif message == Message.DATA:
            self.dataList[(macAP, macClient)] += 1
            self.dataListAP[macAP] += 1
            self.dataListClient[macClient] += 1
        elif message == Message.BEACON:
            self.beaconList[(macAP, macClient)] += 1
            self.beaconAP[macAP] += 1
            self.beaconClient[macClient] += 1
        #elif message == Message.NUM_PACK:
        self.numPack[(macAP, macClient)] += 1
        self.numPackAP[macAP] += 1
        self.numPackClient[macClient] += 1
            
        self.checkEssid(macAP, macClient)
        self.checkEssidAP(macAP, macClient)
        self.checkEssidClient(macAP, macClient)


    def sniffmgmt(self,p):
        #p.show()
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
            if (not from_DS and to_DS):
                macAP = p.addr1
                if p.addr1 != p.addr2:
                    macClient = p.addr2
                else:
                    macClient = None
                    
                #self.createArray(macAP,macClient)
                #self.numPack[macAP,macClient] += 1
                
                self.createArrayAndUpdateInfo(macAP, macClient, Message.NUM_PACK)
                self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                
                #self.checkEssid(p.addr1, p.addr2)
            elif from_DS and not to_DS:
                macAP = p.addr2
                if p.addr3 != p.addr2:
                    macClient = p.addr3
                else:
                    macClient = None
                #self.createArray(macAP, macClient)
                #self.numPack[macAP, macClient] += 1
                
                self.createArrayAndUpdateInfo(macAP, macClient, Message.NUM_PACK)
                self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
            elif not from_DS and not to_DS:
                macAP = p.addr3
                if p.addr3 != p.addr2:
                    macClient = p.addr2
                else:
                    macClient = None
                #print macAP, " ", macClient
                #self.createArray(macAP,macClient)
                #self.numPack[macAP,macClient] += 1
                
                self.createArrayAndUpdateInfo(macAP, macClient, Message.NUM_PACK)
                self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                
                #self.checkEssid(p.addr3, p.addr1)
            #p.show()
            
            if p.haslayer(Dot11) and hasattr(p, 'info'):
                #ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
                activeAp = 1
                if p.addr3 not in self.apPresent:
                    self.apPresent[p.addr3] = []
                self.essid[p.addr3] = p.info
                self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.NUM_PACK)
                self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                #self.createArray(p.addr3, p.addr2)
                
                #print p.info, " ", p.addr1, " ", p.addr2, " ", p.addr3, " ", from_DS, " ", to_DS," ", p.type, " ", p.subtype
                
                #self.checkEssid(p.addr3, p.addr2)
                #self.printInfo(self.essid[p.addr3], p.addr3, p.addr2)
            
            
            if from_DS and not to_DS and p.addr3 != SniffPackage.BROADCAST_ADDR and p.addr1 != SniffPackage.BROADCAST_ADDR:
                key = "%s" % (p.addr3)
                self.createArray(key, p.addr1)
                self.checkFrequence(key, p.addr1,p.dBm_AntSignal)
                #self.checkEssid(key, p.addr1)
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
                    #self.checkEssid(key, p.addr2)
                    #if key in self.essid:
                        #self.printInfo(self.essid[key],key,p.addr2)
                    #else:
                        #self.printInfo("<hidden>",key,p.addr2)
            
            
            if p.haslayer(EAP):
                if p["EAP":].code == 3: # -----------------------> SUCCESS
                    if (p.addr2,p.addr1) not in self.eapHandshakeSuccess:
                        self.createArray(p.addr2, p.addr1)
                    if not from_DS and to_DS:
                        self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.HAND_SUCC)
                        self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    elif from_DS and not to_DS:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.HAND_SUCC)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    elif not from_DS and not to_DS:
                        self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.HAND_SUCC)
                        self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                    ##self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.HAND_SUCC)
                    #self.checkEssid(p.addr2, p.addr1)
                    #self.printInfo(self.essid[p.addr2],p.addr2,p.addr1)
                    return
                elif p["EAP":] == 4: # --------------------> FAILED
                    if not from_DS and to_DS:
                        self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.HAND_FAIL)
                        self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    elif from_DS and not to_DS:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.HAND_FAIL)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    elif not from_DS and not to_DS:
                        self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.HAND_FAIL)
                        self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                    
                    #if (p.addr2,p.addr1) in self.eapRequest:
                        #self.eapHandshakeSuccess[(p.addr2,p.addr1)] = 0
                        #self.eapRequest[(p.addr2,p.addr1)] = 0
                    ##self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.HAND_FAIL)
                    #self.checkEssidClient(p.addr2, p.addr1)
                    #self.checkEssid(p.addr2, p.addr1)
                    return
            
            if hasattr(p, 'type') and p.type == 2 and hasattr(p, 'subtype') and p.subtype == 8:   #BEACON
                #p.show()
                if not from_DS and to_DS:
                    self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.BEACON)
                    self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    
                elif from_DS and not to_DS:
                    self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.BEACON)
                    self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                elif not from_DS and not to_DS:
                    self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.BEACON)
                    self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                    
                    #self.checkEssid(p.addr2, p.addr1)
                return
            if hasattr(p, 'type') and p.type == 2 and hasattr(p, 'subtype') and p.subtype == 0:   #DATA
                #p.show()
                if not from_DS and to_DS:
                    self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.DATA)
                    self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    #self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.NUM_PACK)
                    #self.checkEssid(p.addr1, p.addr2)
                elif from_DS and not to_DS:
                    self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.DATA)
                    self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    #self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.NUM_PACK)
                    #self.checkEssid(p.addr3, p.addr1)
                elif not from_DS and not to_DS:
                    self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.DATA)
                    self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                    #self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.NUM_PACK)
                    
                return
                    
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 11:   #RTS
                #p.show()
                #if not from_DS and to_DS:
                    #self.createArray(macAP, macClient)
                    #self.rtsList[macAP, macClient] += 1
                    
                    #self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.RTS)
                    
                    #self.checkEssid(macAP, macClient)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                #elif from_DS and not to_DS:
                    #self.createArray(p.addr3,p.addr1)
                    #self.rtsList[p.addr3,p.addr1] += 1   
                #if p.addr2 in self.apPresent: 
                self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.RTS)
                self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                #else:
                    #self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.RTS)
                    #self.checkEssid(p.addr3, p.addr1)
                #elif  not from_DS and not to_DS:
                    #self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.RTS)
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 12:   #CTS
                #if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    #self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.CTS)
                    #self.checkEssid(p.addr1, p.addr2)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                #elif from_DS and not to_DS:
                    #self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.CTS)
                    #self.checkEssid(p.addr3, p.addr1)
                #self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.CTS)
                
                if p.addr1 != None:
                    if p.addr1 in self.apPresent:
                        self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.CTS)
                        self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    else:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.CTS)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
            if hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 13:   #ACK

                if p.addr1 != None:
                    if p.addr1 in self.apPresent:
                        self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.ACK)
                        self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    else:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.ACK)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                
                #if (not from_DS and to_DS) or (not from_DS and not to_DS):
                    #self.createArray(p.addr1,p.addr2)
                    #self.ackList[p.addr1,p.addr2] += 1   
                    #self.checkEssid(p.addr1, p.addr2)
                    ##self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                #elif from_DS and not to_DS:
                    #self.createArray(p.addr3,p.addr1)
                    #self.ackList[p.addr3,p.addr1] += 1   
                    #self.checkEssid(p.addr3, p.addr1)
                
                return
                    #self.printInfo(self.essid[p.addr3],p.addr3,p.addr1)
                    
            
            
            if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 11:   #AUTH
                #p.show()
                if p.addr1 in self.apPresent:
                    macAP = p.addr1
                    macClient = p.addr2
                else:
                    macAP = p.addr2
                    macClient = p.addr1
                    
                #if p.addr1 in apPresent:
                    #if p.addr2 not in apPresent[p.addr1]:
                        #apPresent[p.addr1].append(p.addr2);
                
                self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                
                self.createArrayAndUpdateInfo(macAP, macClient, Message.AUTH)
                #self.checkEssid(macAP, macClient)
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
                        
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                    #self.printInfo(self.essid[p.addr1],p.addr1,p.addr2)
                    #self.checkEssid(macAP, macClient)
                    
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.DEAUTH)
                return
                    
            if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 4:   #PROBE_REQ
                if p.addr1 in self.apPresent:
                    macAP = p.addr1
                    macClient = p.addr2
                else:
                    macAP = p.addr2
                    macClient = p.addr1
                self.createArray(macAP,macClient)
                #if p.info == "":
                    #p.info = "-"
                if macAP in self.essid:
                    p.info = self.essid[macAP]
                if (p.info,macClient) not in self.probeRequest:
                    self.probeRequest[(p.info,macClient)] = 0
                self.probeRequest[(p.info,macClient)] += 1
                self.checkFrequence(macAP,macClient,p.dBm_AntSignal)
                #self.enter = True
                #self.checkEssid(p.addr1, p.addr2)
                
                self.createArrayAndUpdateInfo(macAP, macClient, Message.PROBE_REQ)
                
                #self.printInfo(p.info,p.addr1,p.addr2)
                return
            

        #self.printInfo(p.info,p.addr1,p.addr2)


    def takePack(self):
        return self.packages

    def printClientConnect(self):
        for key in self.apPresent:
            print "NUM CLIENT CONNECT IN AP: "+ key + " ", len(self.apPresent[key])
            for c in self.apPresent[key]:
                print c
