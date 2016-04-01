#!/usr/bin/python

from scapy.all import *
import argparse

import interfaceScript
import subprocess

apPresent = {}

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='APMonitoring.py')
    parser.add_argument('-i', '--interface', dest='interface', type=str, required=True, help='Interface to use for sniffing')
    parser.add_argument('-f', '--file', dest='file', type=str, required=False, help='File to read for sniffing')
    parser.add_argument('-b', '--bssid', dest='bssid', type=str, required=False, help='Bssid to set')
    parser.add_argument('-c', '--channel', dest='channel', type=str, required=False, help='Channel to set')
    args = parser.parse_args()
    #networks = {}
    #stop_sniff = False
    print 'Press CTRL+c to stop sniffing..'
    #print '='*150 + '\n{0:20}\t{1:30}\t{2:20}\t{3:1}\t{4:1}\t{5:1}\t{6:1}\t{7:1}\t{8:1}\t{9:1}\n'.format('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT') + '='*150
    
    #if args.channel != None:
        #subprocess.call("ifconfig "+ args.interface +" down", shell=True)
        #subprocess.call("ifconfig -a", shell=True)
        #subprocess.call("iwconfig "+ args.interface +" channel "+ args.channel, shell=True)
        #subprocess.call("ifconfig "+ args.interface +" up", shell=True)
        
    #def s():
    interfaceScript.createTable('ESSID              ','BSSID            ','STATION          ', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ','HAND_SUCC','HAND_FAIL','CORRUPT')
    sniff(iface=args.interface, prn=interfaceScript.sniffmgmt)
    
    
    #print "\nNUM AP: ", len(apPresent),"\n"

    #for key in apPresent:
        #print "\nMAC_AP: "+key
        #print "MAC_CLIENT:"
        #for k in apPresent[key]:
            #print k

    print "\n\n"
    
    
    interfaceScript.printClientConnect()

