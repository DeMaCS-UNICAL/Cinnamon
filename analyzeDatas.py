#!/usr/bin/python

import analyzePackage

class AnalyzeDatas:
    
    def __init__(self, analyze):
        #self.analyze = analyze
        self.info = analyze.takeInformation()
        self.infoAP = analyze.takeInformationAP()
        self.infoClient = analyze.takeInformationClient()
        
        self.contUfficialAP = 0
        self.contRogueAP = 0
        
        self.auth = {}
        self.deauth = {}
        self.disass = {}
        
        
    def analyze(self):
        DATA = open("DATA.txt", "a")
        
        DATA.write("CHANNEL STATION:\n")
        for data in self.infoClient:
            #print self.infoClient[data][3]
            DATA.write(data+" --> "+ str(self.infoClient[data][3])+"\n")
            #if int(self.infoClient[data][4]) > 0:
                #self.auth[data] = self.infoClient[data][4]
            #if int(self.infoClient[data][5]) > 0:
                #self.deauth[data] = self.infoClient[data][5]
            #if int(self.infoClient[data][8]) > 0:
                #self.disass[data] = self.infoClient[data][8]
        
        DATA.write("CHANNEL AP:\n")
        for data in self.infoAP:
            #print self.infoClient[data][3]
            DATA.write(data+" --> "+ str(self.infoAP[data][3])+"\n")
            if self.infoAP[data][0] == "eduroam-wifiunical":
                self.contUfficialAP += 1
            else:
                self.contRogueAP += 1
                
            if int(self.infoAP[data][4]) > 0:
                self.auth[data] = self.infoAP[data][4]
            if int(self.infoAP[data][5]) > 0:
                self.deauth[data] = self.infoAP[data][5]
            if int(self.infoAP[data][8]) > 0:
                self.disass[data] = self.infoAP[data][8]
            
        DATA.write("\n\n")
        DATA.write("CONT CLIENT: "+str(len(self.infoClient))+"\n")
        DATA.write("CONT AP: "+str(len(self.infoAP))+"\n")
        DATA.write("CONT UFFICIAL AP: "+str(self.contUfficialAP)+"\n")
        DATA.write("CONT ROGUE AP: "+str(self.contRogueAP)+"\n")
        
        DATA.write("\n\n")
        DATA.write("CORRUPT PACKAGE CLIENT:  MAC-PERCENTAGE-CORRUPT-TOT\n")
        
        for data in self.infoClient:
            cont = 0
            if int(self.infoClient[data][12]) > 40:
                DATA.write("\n")
                DATA.write(data+" --> "+str(self.infoClient[data][12])+"%\t"+str(self.infoClient[data][11])+"\t"+str(self.infoClient[data][20])+"\n")
                for macAP,macClient in self.info:
                    if macClient == data:
                        if cont < 1:
                            DATA.write("\t\tSPECIFICHE: BSSID-POWER-PERCENTAGE-CORRUPT-TOT\n")
                            cont += 1
                        DATA.write("\t\t\t"+str(self.info[macAP,macClient][1])+"\t"+str(self.info[macAP,macClient][12])+"\t"+str(self.info[macAP,macClient][10])+"\t"+str(self.info[macAP,macClient][11])+"\t"+str(self.info[macAP,macClient][20])+"\n")
        
        DATA.write("\n")
        DATA.write("CORRUPT PACKAGE AP:  BSSID-POWER-PERCENTAGE-CORRUPT-TOT\n")
        
        for data in self.infoAP:
            if int(self.infoAP[data][12]) > 40:
                DATA.write(data+" --> "+str(self.infoAP[data][11])+"\t"+str(self.infoAP[data][13])+"%\t"+str(self.infoAP[data][12])+"\t"+str(self.infoAP[data][21])+"\n")  
        
        
        DATA.write("\n\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("AUTH AP: \n")
        for data in self.auth:
            DATA.write(data+" --> "+str(self.auth[data])+"\n")
            
            
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("DEAUTH AP: \n")
        for data in self.deauth:
            DATA.write(data+" --> "+str(self.deauth[data])+"\n")
            
            
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("DISASS AP: \n")
        for data in self.disass:
            DATA.write(data+" --> "+str(self.disass[data])+"\n")
        
        DATA.close()
        
        
        
        
