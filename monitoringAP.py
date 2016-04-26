#!/usr/bin/python

import scapy
from scapy.all import *

import os

import argparse, sys, thread, time
from time import sleep
import printerInfo
import detachPack
import subprocess
import saving

apPresent = {}

name = "CAPT-"
extension = ".pcap"
contFile = 1

#def tryThis(p):
    #a = str(p).encode('hex')
    #subprocess.call(a +"> a.txt", shell=True)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='APMonitoring.py')
    parser.add_argument('-i', '--interface', dest='interface', type=str, required=False, help='Interface to use for sniffing')
    parser.add_argument('-f', '--file', dest='file', type=str, required=False, help='File to read for sniffing')
    #parser.add_argument('-r', '--read', action='store_true', help='File to read for sniffing after execute -i command')
    #parser.add_argument('-s', '--snifferFile', dest='snifferFile', type=str, required=False, help='File to read for sniffing')
    parser.add_argument('-b', '--bssid', dest='bssid', type=str, required=False, help='Bssid to set')
    parser.add_argument('-c', '--channel', dest='channel', type=str, required=False, help='Channel to set')
    parser.add_argument('-s', '--save', action='store_true', help='Save the capture')
    args = parser.parse_args()
    
    user = os.getenv("SUDO_USER")
    
    if user is None:
        print "This program needs 'sudo'"
    else:
        print 'Press CTRL+c to stop sniffing...'
      
        
        #subprocess.call("ifconfig "+ args.interface +" down", shell=True)
        #subprocess.call("iwconfig "+ args.interface +" mode monitor", shell=True)
        #subprocess.call("ifconfig "+ args.interface +" up", shell=True)
        
        filterStr = ""
        if args.channel != None:
            #subprocess.call("ifconfig "+ args.interface +" down", shell=True)
            #subprocess.call("ifconfig -a", shell=True)
            subprocess.call("iwconfig "+ args.interface +" channel "+ args.channel, shell=True)
            #subprocess.call("ifconfig "+ args.interface +" up", shell=True)
        
        if args.bssid != None:
            filterStr = "wlan src "+args.bssid+" or wlan dst "+args.bssid
            
        #def s():

        if args.file != None:
            import interfaceScript
            printerInfo = printerInfo.PrinterInfo(1, "Thread1", 2)
            printerInfo.start()
            sniffPack = interfaceScript.SniffPackage(printerInfo)

            sniff(offline=args.file, prn=sniffPack.sniffmgmt)
            
            printerInfo.endOfflineSniff(True)
            sys.exit(0)
            
        if args.interface != None:

            if args.save == True:
                
                nameFile = name+str(contFile)+extension
                existFile = os.path.exists(nameFile)

                while existFile:
                    contFile += 1
                    nameFile = name+str(contFile)+extension
                    existFile = os.path.exists(nameFile)
                    
                detachPack = detachPack.DetachPack(nameFile)
                
                savingPack = saving.Saving(2, "Thread3", 2, detachPack, args.interface)
                savingPack.start()
                
                subprocess.call("./monitoringAP.py -f "+nameFile, shell=True)
                
                sys.exit(0)
                
            else:
                import interfaceScript
                printerInfo = printerInfo.PrinterInfo(1, "Thread2", 2)
                printerInfo.start()
                sniffPack = interfaceScript.SniffPackage(printerInfo)
                
                if filterStr != "":
                    sniff(filter=filterStr, iface=args.interface, prn=sniffPack.sniffmgmt)
                else:
                    sniff(iface=args.interface, prn=sniffPack.sniffmgmt)
            #sniff(filter="wlan src 00:80:48:62:dd:13 or wlan dst 00:80:48:62:dd:13", iface=args.interface, prn=sniffPack.sniffmgmt)
    
    #print "\nNUM AP: ", len(apPresent),"\n"

    #for key in apPresent:
        #print "\nMAC_AP: "+key
        #print "MAC_CLIENT:"
        #for k in apPresent[key]:
            #print k

    
    

