#!/usr/bin/python

import scapy
from scapy.all import *

import os, signal

import argparse, sys, thread, time
from time import sleep
import printerInfo
import detachPack
import subprocess
import saving

class bcolors:
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

apPresent = {}
monitors = []
interfaces = {}

name = "CAPT-"
extension = ".pcap"
contFile = 1
#pid = 0

printer = printerInfo.PrinterInfo(1, "Thread2", 2)
#def tryThis(p):
    #a = str(p).encode('hex')
    #subprocess.call(a +"> a.txt", shell=True)

def readInterface():
    DN = open(os.devnull, 'w')
    try:
        proc = subprocess.Popen(['iwconfig'], stdout=PIPE, stderr=DN, shell=True)
        #procPid = proc.pid
    except OSError:
        sys.exit('Could not execute "iwconfig"')
    for line in proc.communicate()[0].split('\n'):
        #print line
        if len(line) == 0: continue # Isn't an empty string
        if line[0] != ' ': # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search: # Isn't wired
                iface = line[:line.find(' ')] # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    #os.kill(procPid,signal.SIGKILL)
    return
    #proc.kill()

def stopperCheck(p):
    if printer.getStopSniff(): 
        return True
    return False

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='APMonitoring.py')
    parser.add_argument('-i', '--interface', dest='interface', type=str, required=False, help='Interface to use for sniffing')
    parser.add_argument('-f', '--file', dest='file', type=str, required=False, help='File to read for sniffing')
    parser.add_argument('-b', '--bssid', dest='bssid', type=str, required=False, help='Bssid to set')
    parser.add_argument('-c', '--channel', dest='channel', type=str, required=False, help='Channel to set')
    parser.add_argument('-s', '--save', action='store_true', help='Save the capture')
    args = parser.parse_args()
    
    user = os.getenv("SUDO_USER")
    
    if user is None:
        print "This program needs 'sudo'"
    else:
        print 'Press CTRL+c to stop sniffing...'
      
        filterStr = ""
        if args.channel != None:
            #subprocess.call("ifconfig "+ args.interface +" down", shell=True)
            #subprocess.call("ifconfig -a", shell=True)
            subprocess.call("iwconfig "+ args.interface +" channel "+ args.channel, shell=True)
            #subprocess.call("ifconfig "+ args.interface +" up", shell=True)
        
        if args.bssid != None:
            filterStr = "wlan src "+args.bssid+" or wlan dst "+args.bssid
            
        #def s():
        
        #if args.pid != None:
            #pid = args.pid

        if args.file != None:
            import interfaceScript
            #printer = None
            printer = printerInfo.PrinterInfo(1, "Thread1", 2)
            printer.start()
            sniffPack = interfaceScript.SniffPackage(printer)

            sniff(offline=args.file, prn=sniffPack.sniffmgmt, stop_filter=stopperCheck)
            #os.kill(pid, signal.SIGKILL)
            #printer.endOfflineSniff(True)
            
        if args.interface != None:

            readInterface()
            #print monitors
            #print interfaces
            if args.interface not in interfaces and args.interface not in monitors:
                print bcolors.FAIL + "The interface in not present\n" + bcolors.ENDC

                os.system('stty sane')
            else:
                try:
                    subprocess.call("ifconfig "+ args.interface +" down", shell=True)
                    subprocess.call("iwconfig "+ args.interface +" mode monitor", shell=True)
                    subprocess.call("ifconfig "+ args.interface +" up", shell=True)
                except Exception:
                    sys.exit('Could not start monitor mode')

                if args.save == True:
                    
                    nameFile = name+str(contFile)+extension
                    existFile = os.path.exists(nameFile)

                    while existFile:
                        contFile += 1
                        nameFile = name+str(contFile)+extension
                        existFile = os.path.exists(nameFile)
                        
                    detachP = detachPack.DetachPack(nameFile)
                    
                    savingPack = saving.Saving(2, "Thread2", 2, detachP, args.interface)
                    savingPack.start()
                    
                    pid = os.getpid()
                    #nameFile = "path.fifo"
                    p = subprocess.call("./monitoringAP.py -f "+nameFile, shell=True)
                    #os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                    detachP.setStopSniff(True)
                    #os.system('stty sane')
                    os.kill(pid,signal.SIGKILL)
                    #sys.exit(0)
                    
                else:
                    import interfaceScript
                    ##printer = None
                    printer = printerInfo.PrinterInfo(1, "Thread1", 2)
                    printer.start()
                    sniffPack = interfaceScript.SniffPackage(printer)
                    
                    if filterStr != "":
                        sniff(filter=filterStr, iface=args.interface, prn=sniffPack.sniffmgmt, stop_filter=stopperCheck)
                    else:
                        sniff(iface=args.interface, prn=sniffPack.sniffmgmt, stop_filter=stopperCheck)
            #sniff(filter="wlan src 00:80:48:62:dd:13 or wlan dst 00:80:48:62:dd:13", iface=args.interface, prn=sniffPack.sniffmgmt)
    
    #print "\nNUM AP: ", len(apPresent),"\n"

    #for key in apPresent:
        #print "\nMAC_AP: "+key
        #print "MAC_CLIENT:"
        #for k in apPresent[key]:
            #print k

    
    

