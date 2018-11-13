#!/usr/bin/python

from scapy.all import *

import time, datetime

from collections import OrderedDict
from db import DB_Manager
from Enum_Type import Enum_Type


class Sniffer:
	def __init__(self):
		self.DB_Man = DB_Manager()
		self.channel = {
			2412 : 1,
			2417 : 2,
			2422 : 3,
			2427 : 4,
			2432 : 5,
			2437 : 6,
			2442 : 7,
			2447 : 8,
			2452 : 9,
			2457 : 10,
			2462 : 11,
			2467 : 12,
			2472 : 13
		}
        
	def sniffAP(self, p):
		timestamp = datetime.datetime.now().isoformat()

		if ( (p.haslayer(Dot11Beacon))):
			ssid = p[Dot11Elt].info
			bssid = p[Dot11FCS].addr3	

			channel = self.channel[p.Channel] if p.haslayer(Dot11Elt) else 'n/a'
			capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
					{Dot11ProbeResp:%Dot11ProbeResp.cap%}")

			type_ = Enum_Type.type_packet[p[Dot11FCS].type]
			subtype = Enum_Type.subtypes_management[p[Dot11FCS].subtype]

			packet_signal = None
			packet_signal = p.dBm_AntSignal
			
			if re.search("privacy", capability): enc = 'Y'
			else: enc  = 'N'

			#p.show()

			record = OrderedDict([
				('access_point_name', ssid),
				('access_point_address', bssid),
				('channel', channel),
				('type', type_),
				('subtype', subtype),
				('strength', packet_signal),
				('timestamp', timestamp)
			])

			if not self.DB_Man.exists_AP(bssid):
				self.DB_Man.insert_Ap(record);
			else:
				if packet_signal is not None:
					self.DB_Man.update_signal_AP(packet_signal, bssid)
				if channel != 'n/a':
					self.DB_Man.update_channel_AP(channel, bssid)
					#TODO Magari se si verificano entrambe, fare solo un metodo
					
		channel = self.channel[p.Channel] if p.haslayer(Dot11Elt) else 'n/a'
		capability = p.sprintf("{Dot11ProbeResp:%Dot11ProbeResp.cap%}") if p.haslayer(Dot11ProbeResp) else 'n/a'
		#print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])
		type_ = Enum_Type.type_packet[p[Dot11FCS].type]
		#print(p[Dot11].subtype)
		subtype = Enum_Type.subtypes_management[p[Dot11FCS].subtype]
		packet_signal = None
		packet_signal = p.dBm_AntSignal

		if hasattr(p, 'FCfield') and p.FCfield is not None:
			DS = p.FCfield & 0x3
			to_DS = DS & 0x1 != 0
			from_DS = DS & 0x2 != 0

		if to_DS and not from_DS:
			BSSID = p[Dot11FCS].addr1
			source = p[Dot11FCS].addr2
			destination = p[Dot11FCS].addr3
		elif not to_DS and from_DS:
			BSSID = p[Dot11FCS].addr2
			destination = p[Dot11FCS].addr1
			source = p[Dot11FCS].addr3
		elif not to_DS and not from_DS:
			destination = p[Dot11FCS].addr1
			source = p[Dot11FCS].addr2
			BSSID = p[Dot11FCS].addr3

		if BSSID == None: BSSID = 'n/a'
		if source == None: source = 'n/a'
		if destination == None: destination = 'n/a'

		if re.search("privacy", capability): enc = 'Y'
		else: enc  = 'N'

		record = OrderedDict([
			('BSSID', BSSID),
			('source', source),
			('destination', destination),
			('channel', channel),
			('type', type_),
			('subtype', subtype),
			('strength', packet_signal),
			('encrypted', enc),
			('to_DS', to_DS),
			('from_DS', from_DS),
			('timestamp', timestamp)
		])

		self.DB_Man.insert_Packet(record);

		if p.haslayer(EAP):	#AUTHENTICATION is in a Beacon!!!!
			type_ = Enum_Type.eap_types[p[EAP].type]
			code = Enum_Type.eap_codes[p[EAP].code]
			record = OrderedDict([
				('BSSID', BSSID),
				('source', source),
				('destination', destination),
				('channel', channel),
				('type', type_),
				('code', code),
				('strength', packet_signal),
				('encrypted', enc),
				('to_DS', to_DS),
				('from_DS', from_DS),
				('timestamp', timestamp)
			])
			#print(record)
			self.DB_Man.insert_EAP(record)
