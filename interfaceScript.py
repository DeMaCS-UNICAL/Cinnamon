#!/usr/bin/python

import scapy
import scapy_ex
import os,sys
import printerInfo

import enum
from enum import Enum

from scapy.all import *
import time, datetime
#from time import sleep


class Message(Enum):
    AUTH = "0"
    DEAUTH = "1"

    PROBE_REQ = "2"
    PROBE_RESP = "3"
    
    HAND_SUCC = "4"
    HAND_FAIL = "5"
    
    CORR_PACK = "6"
    RTS = "7"

    CTS = "8"
    ACK = "9"

    DATA = "10"
    BEACON = "11"
    
    ASSOC_REQ = "12"
    ASSOC_RESP = "13"
    DISASSOC = "14"
    
    NUM_PACK = "15"
    
    OTHER = "16"


class SniffPackage:
    
    BROADCAST_ADDR = "ff:ff:ff:ff:ff:ff"
    EXTENSION_LOG = ".log"
    FOLDER_LOG = "log/"
    
    def __init__(self, printerInfo):
        self.apPresent = []

        self.essid = {}
        #channel = {}

        self.frequence = {}

        self.authent = {}
        self.authentAP = {}
        self.authentClient = {}
        
        self.associationRequest = {}
        self.associationRequestAP = {}
        self.associationRequestClient = {}
        
        self.associationResponce = {}
        self.associationResponceAP = {}
        self.associationResponceClient = {}

        self.disassociation = {}
        self.disassociationAP = {}
        self.disassociationClient = {}
        
        self.deauthent = {}
        self.deauthentAP = {}
        self.deauthentClient = {}
        
        self.probeRequest = {}
        self.probeRequestAP = {}
        self.probeRequestClient = {}
        
        self.probeResponse = {}
        self.probeResponseAP = {}
        self.probeResponseClient = {}
        
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
        
        self.otherList = {}
        self.otherListAP = {}
        self.otherListClient = {}
        
        self.cont = 0
        self.printerInfo = printerInfo
        
        self.info = {}
        self.infoAP = {}
        self.infoClient = {}
        
        self.contForAP = 0
        
        now = datetime.datetime.now()
        date = str(now.year)+str(now.month)+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)+"-"+str(now.second)
        self.titleLog = SniffPackage.FOLDER_LOG + date + SniffPackage.EXTENSION_LOG
        self.fileLog = open(self.titleLog, "w+")

    def createArray(self,macAP, macClient):
        if (macAP,macClient) not in self.deauthent:
            self.deauthent[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.authent:
            self.authent[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.associationRequest:
            self.associationRequest[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.associationResponce:
            self.associationResponce[(macAP,macClient)] = 0
        if (macAP,macClient) not in self.disassociation:
            self.disassociation[(macAP,macClient)] = 0
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
        if (macAP,macClient) not in self.probeResponse:
            self.probeResponse[(macAP,macClient)] = 0
        if macClient not in self.ackList:
            self.ackList[macClient] = 0
        if (macAP,macClient) not in self.otherList:
            self.otherList[(macAP,macClient)] = 0
        
    
    def createArrayAP(self, macAP):
        if macAP not in self.beaconAP:
            self.beaconAP[macAP] = 0
        if macAP not in self.numPackAP:
            self.numPackAP[macAP] = 0
        if macAP not in self.authentAP:
            self.authentAP[macAP] = 0
        if macAP not in self.associationRequestAP:
            self.associationRequestAP[macAP] = 0
        if macAP not in self.associationResponceAP:
            self.associationResponceAP[macAP] = 0
        if macAP not in self.disassociationAP:
            self.disassociationAP[macAP] = 0
        if macAP not in self.deauthentAP:
            self.deauthentAP[macAP] = 0
        if macAP not in self.probeRequestAP:
            self.probeRequestAP[macAP] = 0
        if macAP not in self.probeResponseAP:
            self.probeResponseAP[macAP] = 0
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
        if macAP not in self.otherListAP:
            self.otherListAP[macAP] = 0
            
    def createArrayClient(self, macClient):
        if macClient not in self.beaconClient:
            self.beaconClient[macClient] = 0
        if macClient not in self.numPackClient:
            self.numPackClient[macClient] = 0
        if macClient not in self.authentClient:
            self.authentClient[macClient] = 0
        if macClient not in self.associationRequestClient:
            self.associationRequestClient[macClient] = 0
        if macClient not in self.associationResponceClient:
            self.associationResponceClient[macClient] = 0
        if macClient not in self.disassociationClient:
            self.disassociationClient[macClient] = 0
        if macClient not in self.deauthentClient:
            self.deauthentClient[macClient] = 0
        if macClient not in self.probeRequestClient:
            self.probeRequestClient[macClient] = 0
        if macClient not in self.probeResponseClient:
            self.probeResponseClient[macClient] = 0
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
        if macClient not in self.otherListClient:
            self.otherListClient[macClient] = 0
    
    

    def checkFrequence(self,macAP, macClient,freq):
        if freq != 0 and freq != None:
            if macAP != SniffPackage.BROADCAST_ADDR:
                self.frequence[(macAP,macClient)] = freq

    def printInfo(self,essid,macAP,macClient):
        if macAP != None and macClient != None:
            if (essid,macClient) not in self.probeRequest:
                self.probeRequest[(essid,macClient)] = 0

            if self.numPack[(macAP,macClient)] != 0:
                percentCorr = int(float(self.corruptedPack[(macAP,macClient)])/float(self.numPack[(macAP,macClient)])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authent[(macAP,macClient)], self.deauthent[(macAP,macClient)], self.associationRequest[(macAP,macClient)], self.associationResponce[(macAP,macClient)], self.disassociation[(macAP,macClient)], self.frequence[(macAP,macClient)], self.eapHandshakeSuccess[(macAP,macClient)], self.eapHandshakeFailed[(macAP,macClient)], self.corruptedPack[(macAP,macClient)], strPercentage, self.dataList[(macAP,macClient)], self.rtsList[(macAP,macClient)], self.ctsList[(macAP,macClient)], self.ackList[(macAP, macClient)], self.beaconList[(macAP,macClient)],  self.probeRequest[(essid,macClient)], self.probeResponse[(macAP,macClient)], self.numPack[(macAP,macClient)], self.otherList[(macAP,macClient)]])
            
            #self.info[i[1],i[2]] = i
            self.printerInfo.addInfo(i)
    
    
    def printInfoAP(self, essid, macAP, macClient):
        if macAP != None and macAP != SniffPackage.BROADCAST_ADDR and macClient != None:
            if (macAP) not in self.probeRequestAP:
                self.probeRequestAP[macAP] = 0

            if self.numPackAP[macAP] != 0:
                percentCorr = int(float(self.corruptedPackAP[macAP])/float(self.numPackAP[macAP])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authentAP[macAP], self.deauthentAP[macAP], self.associationRequestAP[macAP], self.associationResponceAP[macAP], self.disassociationAP[macAP], "-", self.eapHandshakeSuccessAP[macAP], self.eapHandshakeFailedAP[macAP], self.corruptedPackAP[macAP], strPercentage, self.dataListAP[macAP], self.rtsListAP[macAP], self.ctsListAP[macAP], self.ackListAP[macAP], self.beaconAP[macAP],  self.probeRequestAP[macAP], self.probeResponseAP[macAP], self.numPackAP[macAP], self.otherListAP[macAP]])
            
            #self.infoAP[i[1]] = i
            self.printerInfo.addInfoAP(i)
            
    def printInfoClient(self, essid, macAP, macClient):
        if macAP != None and macClient != None:
            if (macClient) not in self.probeRequestClient:
                self.probeRequestClient[macClient] = 0
            
            if self.numPackClient[macClient] != 0:
                percentCorr = int(float(self.corruptedPackClient[macClient])/float(self.numPackClient[macClient])*100)
            
            strPercentage = str(percentCorr)
            
            i = tuple([essid, macAP, macClient, self.authentClient[macClient], self.deauthentClient[macClient], self.associationRequestClient[macClient], self.associationResponceClient[macClient], self.disassociationClient[macClient], "-", self.eapHandshakeSuccessClient[macClient], self.eapHandshakeFailedClient[macClient], self.corruptedPackClient[macClient], strPercentage, self.dataListClient[macClient], self.rtsListClient[macClient], self.ctsListClient[macClient], self.ackListClient[macClient], self.beaconClient[macClient],  self.probeRequestClient[macClient], self.probeResponseClient[macClient], self.numPackClient[macClient], self.otherListClient[macClient]])
            
            #self.infoClient[i[2]] = i
            self.printerInfo.addInfoClient(i)
    
    
    def takeInformation(self):
        return self.info
    
    def takeInformationAP(self):
        return self.infoAP
    
    def takeInformationClient(self):
        return self.infoClient
    
    
    def createArrayForCorruptPack(self, essid, macAP, macClient, hasInfo):
        self.createArrayAndUpdateInfo(macAP, macClient, Message.CORR_PACK)
        
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
                            self.createArrayForCorruptPack("", p.addr1, p.addr2, False)
                elif from_DS and not to_DS:
                    if hasattr(p, 'addr1') and hasattr(p, 'addr2'):
                        if p.addr1 != None and p.addr2 != None:
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

    
    def createArrayAndUpdateInfo(self, macAP, macClient, message, increaseNumPack=True):
        
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
        elif message == Message.PROBE_RESP:
            self.probeResponse[(macAP, macClient)] += 1
            self.probeResponseAP[macAP] += 1
            self.probeResponseClient[macClient] += 1
        elif message == Message.HAND_SUCC:
            self.eapHandshakeSuccess[(macAP, macClient)] += 1
            self.eapHandshakeSuccessAP[macAP] += 1
            self.eapHandshakeSuccessClient[macClient] += 1
        elif message == Message.HAND_FAIL:
            self.eapHandshakeFailed[(macAP, macClient)] += 1
            self.eapHandshakeFailedAP[macAP] += 1
            self.eapHandshakeFailedClient[macClient] += 1
        elif message == Message.CORR_PACK:
            if increaseNumPack:
                self.corruptedPackAP[macAP] += 1
            self.corruptedPack[(macAP, macClient)] += 1
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
            if increaseNumPack:
                self.dataListAP[macAP] += 1
            self.dataList[(macAP, macClient)] += 1
            self.dataListClient[macClient] += 1
        elif message == Message.BEACON:
            if increaseNumPack:
                self.beaconAP[macAP] += 1
            self.beaconList[(macAP, macClient)] += 1
            self.beaconClient[macClient] += 1
        elif message == Message.ASSOC_REQ:
            self.associationRequestAP[macAP] += 1
            self.associationRequest[(macAP, macClient)] += 1
            self.associationRequestClient[macClient] += 1
        elif message == Message.ASSOC_RESP:
            self.associationResponceAP[macAP] += 1
            self.associationResponce[(macAP, macClient)] += 1
            self.associationResponceClient[macClient] += 1
        elif message == Message.DISASSOC:
            self.disassociationAP[macAP] += 1
            self.disassociation[(macAP, macClient)] += 1
            self.disassociationClient[macClient] += 1
        elif message == Message.OTHER:
            self.otherListAP[macAP] += 1
            self.otherList[(macAP, macClient)] += 1
            self.otherListClient[macClient] += 1

        if increaseNumPack:
            self.numPackAP[macAP] += 1
            
        self.numPackClient[macClient] += 1
        self.numPack[(macAP, macClient)] += 1
        
        self.checkEssid(macAP, macClient)
        self.checkEssidAP(macAP, macClient)
        self.checkEssidClient(macAP, macClient)
        
       

    def sniffmgmt(self,p):
        from_DS = None
        to_DS = None
        
        if hasattr(p, 'FCfield') and p.FCfield is not None:
            DS = p.FCfield & 0x3
            to_DS = DS & 0x1 != 0
            from_DS = DS & 0x2 != 0
            
            retry = p.FCfield & 0x8
        
        if self.contForAP > 20:
            isCorrupted = self.checkFCS(p, from_DS, to_DS)
            if isCorrupted:
                return
            #isCorrupted = False
            elif not isCorrupted:
                activeAp = 0
                if p.haslayer(Dot11) and hasattr(p, 'info'):
                    #ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
                    activeAp = 1
                    if p.addr3 not in self.apPresent:
                        self.apPresent.insert(0,p.addr3)
                        #self.apPresent[p.addr3] = []
                    self.essid[p.addr3] = p.info
                    self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                
                if from_DS and not to_DS and p.addr3 != SniffPackage.BROADCAST_ADDR and p.addr1 != SniffPackage.BROADCAST_ADDR:
                    key = "%s" % (p.addr3)
                    self.createArray(key, p.addr1)
                    self.checkFrequence(key, p.addr1,p.dBm_AntSignal)

                elif not from_DS and to_DS and p.addr2 != SniffPackage.BROADCAST_ADDR:
                    key = "%s" % (p.addr1)
                    if key in self.apPresent:
                        self.createArray(key, p.addr2)
                        self.checkFrequence(key,p.addr2,p.dBm_AntSignal)
                
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
                        
                        return
                
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 8:   #BEACON
                    if p.addr2 not in self.apPresent:
                        self.apPresent.insert(0,p.addr2)
                        #self.apPresent[p.addr2] = []
                    if not from_DS and to_DS:
                        self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.BEACON)
                        self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                        
                        self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.BEACON, False)
                        self.checkFrequence(p.addr1, p.addr3,p.dBm_AntSignal)
                        
                    elif from_DS and not to_DS:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.BEACON)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                        
                        self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.BEACON, False)
                        self.checkFrequence(p.addr2, p.addr3,p.dBm_AntSignal)
                    elif not from_DS and not to_DS:
                        isDifferent = False
                        if p.addr3 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.BEACON)
                            self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                            
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr3, None, Message.BEACON)
                        else:
                            self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.BEACON, False)
                        self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                        
                    return
                #elif hasattr(p, 'type') and p.type == 2 and hasattr(p, 'subtype') and p.subtype == 0:   #DATA
                elif hasattr(p, 'type') and p.type == 2:   #DATA
                    isDifferent = False
                    if not from_DS and to_DS:
                        if p.addr1 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.DATA)
                            self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                        
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.DATA)
                        else:
                            if p.addr1 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.DATA, False)
                        self.checkFrequence(p.addr1, p.addr3,p.dBm_AntSignal)
                    elif from_DS and not to_DS:
                        if p.addr1 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.DATA)
                            self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.DATA)
                        else:
                            if p.addr2 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.DATA, False)
                        self.checkFrequence(p.addr2, p.addr3,p.dBm_AntSignal)
                    elif not from_DS and not to_DS:
                        if p.addr3 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.DATA)
                            self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.DATA)
                            self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                        else:
                            if p.addr1 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.DATA, False)
                                self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                        
                    return
                        
                elif hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 11:   #RTS
                    macAP = p.addr2
                    macClient = p.addr1
                    if p.addr1 in self.apPresent:
                        macAP = p.addr1
                        macClient = p.addr2
                    
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.RTS)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                
                    return
                elif hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 12:   #CTS

                    if p.addr1 != None:
                        if p.addr1 in self.apPresent:
                            self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.CTS)
                            self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                        else:
                            self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.CTS)
                            self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    
                    return
                elif hasattr(p, 'type') and p.type == 1 and hasattr(p, 'subtype') and p.subtype == 13:   #ACK
                    
                    if p.addr1 != None:
                        if p.addr1 in self.apPresent:
                            self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.ACK)
                            self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                        else:
                            self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.ACK)
                            self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    
                    return
                
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 11:   #AUTH
                    if retry == 0 and p.addr2 != p.addr3:
                        macAP = p.addr1
                        macClient = p.addr2
                    else:
                        if p.addr2 != p.addr3:
                            macAP = p.addr2
                            macClient = p.addr1
                        else:
                            macAP = p.addr1
                            macClient = p.addr2
                        
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.AUTH)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)                

                    return
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 0:   #ASSOC_REQ
                    macAP = p.addr1
                    macClient = p.addr2

                    self.createArrayAndUpdateInfo(macAP, macClient, Message.ASSOC_REQ)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)                

                    return
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 1:   #ASSOC_RESP
                    macAP = p.addr1
                    macClient = p.addr2
                        
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.DISASSOC)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)                

                    return
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 10:   #DISASSOC
                    macAP = p.addr2
                    macClient = p.addr1
                        
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.ASSOC_RESP)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)                

                    return
                        
                elif hasattr(p, 'type') and hasattr(p, 'subtype') and p.type == 0 and p.subtype == 12:   #DEAUTH
                    if p.addr1 in self.apPresent:
                        macAP = p.addr1
                        macClient = p.addr2
                    else:
                        macAP = p.addr2
                        macClient = p.addr1
                            
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.DEAUTH)
                    self.checkFrequence(macAP, macClient,p.dBm_AntSignal)
                    return
                        
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 4:   #PROBE_REQ
                    macAP = p.addr1
                    macClient = p.addr2

                    if macAP in self.essid:
                        p.info = self.essid[macAP]
                    if (p.info,macClient) not in self.probeRequest:
                        self.probeRequest[(p.info,macClient)] = 0
                    self.probeRequest[(p.info,macClient)] += 1
                    
                    self.createArrayAndUpdateInfo(macAP, macClient, Message.PROBE_REQ)
                    self.checkFrequence(macAP,macClient,p.dBm_AntSignal)
                    
                    return
                
                elif hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 5:   #PROBE_RESP
                    if p.addr2 != None:
                        self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.PROBE_RESP)
                        self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    return
                else:
                    isDifferent = False
                    if not from_DS and to_DS:
                        if p.addr1 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.OTHER)
                            self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                        
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.OTHER)
                        else:
                            if p.addr1 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.OTHER, False)
                        self.checkFrequence(p.addr1, p.addr3,p.dBm_AntSignal)
                
                    elif from_DS and not to_DS:
                        if p.addr1 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.OTHER)
                            self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.OTHER)
                        else:
                            if p.addr2 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.OTHER, False)
                        self.checkFrequence(p.addr2, p.addr3,p.dBm_AntSignal)
                    
                    elif not from_DS and not to_DS:
                        if p.addr3 != p.addr2:
                            isDifferent = True
                            self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.OTHER)
                            self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                        if not isDifferent:
                            self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.OTHER)
                            #self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                        else:
                            if p.addr1 != p.addr3:
                                self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.OTHER, False)
                        self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                    
                    self.fileLog = open(self.titleLog, "a")
                    self.fileLog.write("TYPE - SUBTYPE: ")
                    self.fileLog.write(str(p.type)+ " " + str(p.subtype)+"\n")
                    self.fileLog.write("ADDRESS: ")
                    self.fileLog.write(str(p.addr1)+"   -   " + str(p.addr2)+"   -   " + str(p.addr3)+"\n")
                    self.fileLog.write("FROM_DS - TO_DS: ")
                    self.fileLog.write(str(from_DS)+ " "+ str(to_DS))
                    self.fileLog.write("\n------------------------------------------------------------------\n\n")
                    self.fileLog.close()
                
        else:
            if p.haslayer(Dot11) and hasattr(p, 'info'):
                #ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
                activeAp = 1
                if p.addr3 not in self.apPresent:
                    self.apPresent.insert(0,p.addr3)
                    #self.apPresent[p.addr3] = []
                self.essid[p.addr3] = p.info
                #self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.NUM_PACK)
                self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                self.contForAP += 1
            
            if hasattr(p, 'type') and p.type == 0 and hasattr(p, 'subtype') and p.subtype == 8:   #BEACON
                if p.addr2 not in self.apPresent:
                    self.apPresent.insert(0,p.addr2)
                    #self.apPresent[p.addr2] = []
                if not from_DS and to_DS:
                    self.createArrayAndUpdateInfo(p.addr1, p.addr2, Message.BEACON)
                    self.checkFrequence(p.addr1, p.addr2,p.dBm_AntSignal)
                    
                    self.createArrayAndUpdateInfo(p.addr1, p.addr3, Message.BEACON, False)
                    self.checkFrequence(p.addr1, p.addr3,p.dBm_AntSignal)
                    
                elif from_DS and not to_DS:
                    self.createArrayAndUpdateInfo(p.addr2, p.addr1, Message.BEACON)
                    self.checkFrequence(p.addr2, p.addr1,p.dBm_AntSignal)
                    
                    self.createArrayAndUpdateInfo(p.addr2, p.addr3, Message.BEACON, False)
                    self.checkFrequence(p.addr2, p.addr3,p.dBm_AntSignal)
                elif not from_DS and not to_DS:
                    isDifferent = False
                    if p.addr3 != p.addr2:
                        isDifferent = True
                        self.createArrayAndUpdateInfo(p.addr3, p.addr2, Message.BEACON)
                        self.checkFrequence(p.addr3, p.addr2,p.dBm_AntSignal)
                        
                    if not isDifferent:
                        self.createArrayAndUpdateInfo(p.addr3, None, Message.BEACON)
                    else:
                        self.createArrayAndUpdateInfo(p.addr3, p.addr1, Message.BEACON, False)
                    self.checkFrequence(p.addr3, p.addr1,p.dBm_AntSignal)
                    
                self.contForAP += 1
                return
