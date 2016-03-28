#!/usr/bin/python

from scapy.all import *
import argparse

import interfaceScript

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
    print '='*150 + '\n{0:20}\t{1:30}\t{2:20}\t{3:1}\t{4:1}\t{5:1}\t{6:1}\n'.format('ESSID','BSSID','STATION', 'PROBE_REQ', 'AUTH','DEAUTH', 'FREQ') + '='*150
    
    #def s():
    sniff(iface=args.interface, prn=interfaceScript.sniffmgmt)

    #print "\nNUM AP: ", len(apPresent),"\n"

    #for key in apPresent:
        #print "\nMAC_AP: "+key
        #print "MAC_CLIENT:"
        #for k in apPresent[key]:
            #print k

    print "\n\n"
    
    
    interfaceScript.printClientConnect()

