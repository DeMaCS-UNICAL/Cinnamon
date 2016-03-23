#!/usr/bin/python

from scapy.all import *
import argparse

found = {}
apPresent = {}

def sniffmgmt(p):
	
	DS = p.FCfield & 0x3
        to_DS = DS & 0x1 != 0
        from_DS = DS & 0x2 != 0
        
        activeAp = 0
        
	if p.haslayer(Dot11) and hasattr(p, 'info'):
		ssid = ( len(p.info) > 0 and p.info != "\x00" ) and p.info or '<hidden>'
		
		if ssid == "eduroam-wifiunical":
                    activeAp = 1

        if activeAp == 1:
            if not from_DS and not to_DS and p.addr3 != "ff:ff:ff:ff:ff:ff":
                key = "%s" % (p.addr3)
                if key not in apPresent:
                    apPresent[key] = []
                if p.addr2 not in apPresent[key]:
                    apPresent[key].append(p.addr2)
                    print "MAC_AP: " + key + " ----->  MAC_CLIENT:  " + p.addr2

        elif activeAp == 0:
            if not from_DS and to_DS and p.addr2 != "ff:ff:ff:ff:ff:ff":
                key = "%s" % (p.addr1)
                if key in apPresent:
                    #apPresent[key] = []
                    if p.addr2 not in apPresent[key]:
                        apPresent[key].append(p.addr2)
                        print "MAC_AP: " + key + " ----->  MAC_CLIENT:  " + p.addr2


if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("usage: sniff.py <iface>")
            sys.exit(-1)
        
        parser = argparse.ArgumentParser(description='APMonitoring.py')
        parser.add_argument('-i', '--interface', dest='interface', type=str, required=True, help='Interface to use for sniffing and packet injection')
        args = parser.parse_args()
        print 'Press CTRL+c to stop sniffing..'
    
        #def s():
        sniff(iface=args.interface, prn=sniffmgmt)

        print "\nNUM AP: ", len(apPresent),"\n"

        for key in apPresent:
            print "\nMAC_AP: "+key
            print "MAC_CLIENT:"
            for k in apPresent[key]:
                print k

        print "\n\n"
        for key in apPresent:
            print "NUM CLIENT CONNECT IN AP: "+ key + " ", len(apPresent[key])

