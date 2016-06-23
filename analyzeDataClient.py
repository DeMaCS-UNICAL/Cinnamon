#!/usr/bin/python

import analyzeData
import analyzePackage

class AnalyzeDataClient(analyzeData.AnalyzeData):
    
    
    def __init__(self, analyze):
        analyzeData.AnalyzeData.__init__(self, analyze) 
        self.info = analyze.takeInformation()
        
        self.infoRoamingClient = analyze.takeInformationRoamingClient()
        
        self.channelClient = []
        
        
    def analyzeData(self):
        DATA = open("DATA_STATION.txt", "a")
        
        DATA.write("CHANNEL STATION:\n")
        for data in self.infoClient:
            #print self.infoClient[data][3]
            DATA.write(data+" --> "+ str(self.infoClient[data][3])+"\n")
            if self.infoClient[data][3] not in self.channelClient:
                self.channelClient.append(self.infoClient[data][3])
            
            if int(self.infoClient[data][4]) > 0:
                self.auth[data] = self.infoClient[data][4]
            if int(self.infoClient[data][5]) > 0:
                self.deauth[data] = self.infoClient[data][5]
            if int(self.infoClient[data][6]) > 0:
                self.associationRequest[data] = self.infoClient[data][6]
            if int(self.infoClient[data][7]) > 0:
                self.associationResponce[data] = self.infoClient[data][7]
            if int(self.infoClient[data][8]) > 0:
                self.disass[data] = self.infoClient[data][8]
            if int(self.infoClient[data][9]) > 0:
                self.eapHandshakeSuccess[data] = self.infoClient[data][9]
            if int(self.infoClient[data][10]) > 0:
                self.eapHandshakeFailed[data] = self.infoClient[data][10]
            if int(self.infoClient[data][13]) > 0:
                self.dataList[data] = self.infoClient[data][13]
            if int(self.infoClient[data][14]) > 0:
                self.rts[data] = self.infoClient[data][14]
            if int(self.infoClient[data][15]) > 0:
                self.cts[data] = self.infoClient[data][15]
            if int(self.infoClient[data][16]) > 0:
                self.ack[data] = self.infoClient[data][16]
            if int(self.infoClient[data][17]) > 0:
                self.beacon[data] = self.infoClient[data][17]
            if int(self.infoClient[data][18]) > 0:
                self.probeRequest[data] = self.infoClient[data][18]
            if int(self.infoClient[data][19]) > 0:
                self.probeResponse[data] = self.infoClient[data][19]
            if int(self.infoClient[data][20]) > 0:
                self.numPack[data] = self.infoClient[data][20]
        
        DATA.write("\nALL STATION'S CHANNEL: \n")
        for channel in self.channelClient:
            if channel != "-":
                DATA.write(str(channel)+"  ")
        
            
        DATA.write("\n\n")
        DATA.write("CONT CLIENT: "+str(len(self.infoClient))+"\n")
        
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
                            DATA.write("\t\tSPECIFICHE: BSSID-PERCENTAGE-POWER-CORRUPT-TOT\n")
                            cont += 1
                        DATA.write("\t\t\t"+str(self.info[macAP,macClient][1])+"\t"+str(self.info[macAP,macClient][12])+"%"+"\t"+str(self.info[macAP,macClient][10])+"\t"+str(self.info[macAP,macClient][11])+"\t"+str(self.info[macAP,macClient][20])+"\n")
        

        DATA.write("\n\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("TOT AUTH: "+str(len(self.auth))+" --> AUTH/TOT PACKAGE \n")
        for data in self.auth:
            DATA.write("\t"+data+" --> "+str(self.auth[data])+" / "+str(self.numPack[data])+" \n")
            
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("TOT DEAUTH: "+str(len(self.deauth))+" --> DEAUTH/TOT PACKAGE \n")
        for data in self.deauth:
            DATA.write("\t"+data+" --> "+str(self.deauth[data])+" / "+str(self.numPack[data])+"\n")
            
        DATA.write("\n")
        DATA.write("TOT ASSOCIATION REQUEST: "+str(len(self.associationRequest))+" --> ASSOCIATION REQUEST/TOT PACKAGE \n")
        for data in self.associationRequest:
            DATA.write("\t"+data+" --> "+str(self.associationRequest[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT ASSOCIATION RESPONCE: "+str(len(self.associationResponce))+" --> ASSOCIATION RESPONCE/TOT PACKAGE \n")
        for data in self.associationResponce:
            DATA.write("\t"+data+" --> "+str(self.associationResponce[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("TOT DISASS: "+str(len(self.disass))+" --> DISASS/TOT PACKAGE \n")
        for data in self.disass:
            DATA.write("\t"+data+" --> "+str(self.disass[data])+" / "+str(self.numPack[data])+"\n")
        
        
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("TOT HAND_SHAKE WITH SUCCESS: "+str(len(self.eapHandshakeSuccess))+" --> HAND_SHAKE SUCCESS/TOT PACKAGE \n")
        for data in self.eapHandshakeSuccess:
            DATA.write("\t"+data+" --> "+str(self.eapHandshakeSuccess[data])+" / "+str(self.numPack[data])+"\n")
       
        DATA.write("\n")
        #DATA.write("OTHER VALUE AP:\n")
        DATA.write("TOT HAND_SHAKE FAILED: "+str(len(self.eapHandshakeFailed))+" --> HAND_SHAKE FAILED/TOT PACKAGE \n")
        for data in self.eapHandshakeFailed:
            DATA.write("\t"+data+" --> "+str(self.eapHandshakeFailed[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT PACKAGE DATA: "+ str(len(self.dataList)) +" --> DATA/TOT PACKAGE \n")
        for data in self.dataList:
            DATA.write("\t"+data+" --> "+str(self.dataList[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT RTS: "+str(len(self.rts))+" --> RTS/TOT PACKAGE \n")
        for data in self.rts:
            DATA.write("\t"+data+" --> "+str(self.rts[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT CTS: "+str(len(self.cts))+" --> CTS/TOT PACKAGE \n")
        for data in self.cts:
            DATA.write("\t"+data+" --> "+str(self.cts[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT ACK: "+str(len(self.ack))+" --> ACK/TOT PACKAGE \n")
        for data in self.ack:
            DATA.write("\t"+data+" --> "+str(self.ack[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT BEACON: "+str(len(self.beacon))+" --> BEACON/TOT PACKAGE \n")
        for data in self.beacon:
            DATA.write("\t"+data+" --> "+str(self.beacon[data])+" / "+str(self.numPack[data])+"\n")
        
        
        DATA.write("\n")
        DATA.write("TOT PROBE REQUEST: "+str(len(self.probeRequest))+" --> PROBE REQUEST/TOT PACKAGE \n")
        for data in self.probeRequest:
            DATA.write("\t"+data+" --> "+str(self.probeRequest[data])+" / "+str(self.numPack[data])+"\n")
        
        DATA.write("\n")
        DATA.write("TOT PROBE RESPONCE: "+str(len(self.probeResponse))+" --> PROBE RESPONCE/TOT PACKAGE \n")
        for data in self.probeResponse:
            DATA.write("\t"+data+" --> "+str(self.probeResponse[data])+" / "+str(self.numPack[data])+"\n")

        
        DATA.write("\n")
        DATA.write("ROAMING CLIENT: \n")
        
        contRoaming = 0
        for data in self.infoRoamingClient:
            if len(self.infoRoamingClient[data]) > 1:
                DATA.write(data+": \n")
                contRoaming += 1
                for d in self.infoRoamingClient[data]:
                    DATA.write("\t"+d+"\n")
                DATA.write("\n")
        
        DATA.write("TOT ROAMING CLIENT: "+ str(contRoaming) +"\n")
        
        
        DATA.close()
        





    
    
