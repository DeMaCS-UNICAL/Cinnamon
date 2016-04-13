#!/usr/bin/python

import scapy
from scapy.all import *
import argparse, sys

import printerInfo
import detachPack
import subprocess


apPresent = {}

#def tryThis(p):
    #a = str(p).encode('hex')
    #subprocess.call(a +"> a.txt", shell=True)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='APMonitoring.py')
    parser.add_argument('-i', '--interface', dest='interface', type=str, required=False, help='Interface to use for sniffing')
    parser.add_argument('-f', '--file', dest='file', type=str, required=False, help='File to read for sniffing')
    #parser.add_argument('-s', '--snifferFile', dest='snifferFile', type=str, required=False, help='File to read for sniffing')
    parser.add_argument('-b', '--bssid', dest='bssid', type=str, required=False, help='Bssid to set')
    parser.add_argument('-c', '--channel', dest='channel', type=str, required=False, help='Channel to set')
    parser.add_argument('-s', '--save', action='store_true', help='Save the capture')
    args = parser.parse_args()
    print 'Press CTRL+c to stop sniffing...'
    #print '='*150 + '\n{0:20}\t{1:30}\t{2:20}\t{3:1}\t{4:1}\t{5:1}\t{6:1}\t{7:1}\t{8:1}\t{9:1}\n'.format('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT') + '='*150
    
    if args.channel != None:
        subprocess.call("ifconfig "+ args.interface +" down", shell=True)
        #subprocess.call("ifconfig -a", shell=True)
        subprocess.call("iwconfig "+ args.interface +" channel "+ args.channel, shell=True)
        subprocess.call("ifconfig "+ args.interface +" up", shell=True)
        
    #def s():
    #sniffFile = fileScript.SniffFile()
    

    if args.file != None:
        import interfaceScript
        #index = 0
        printerInfo = printerInfo.PrinterInfo(1, "Thread1", 2)
        printerInfo.start()
        sniffPack = interfaceScript.SniffPackage(printerInfo)

        sniff(offline=args.file, prn=sniffPack.sniffmgmt)

    if args.interface != None:
        #subprocess.call(stri, shell=True)
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            
        #printerInfo.setStopSniff(True)
        
        #sniff(iface="en1",prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%}"))
        #line in sys.stdin:
            #sys.stdout.write(line)

        #for i in sniffPack.takePack():
            #i.show()
    
        print "\n\n"
        #sniffPack.printClientConnect()

        if args.save == True:
            detachPack = detachPack.DetachPack()
            sniff(iface=args.interface, prn=detachPack.detach)
        else:
            import interfaceScript
            printerInfo = printerInfo.PrinterInfo(1, "Thread2", 2)
            printerInfo.start()
            sniffPack = interfaceScript.SniffPackage(printerInfo)
            
            sniff(iface=args.interface, prn=sniffPack.sniffmgmt)
    
    #print "\nNUM AP: ", len(apPresent),"\n"

    #for key in apPresent:
        #print "\nMAC_AP: "+key
        #print "MAC_CLIENT:"
        #for k in apPresent[key]:
            #print k

    
    

