#!/usr/bin/python

from scapy.all import *

import time, datetime

from collections import OrderedDict
from db import DB_Manager
from Enum_Type import Enum_Type


class Sniffer:
	DB_Man = DB_Manager()
	
	def sniffAP(self, p):
		timestamp = datetime.datetime.now().isoformat()

		if ( (p.haslayer(Dot11Beacon))):
			ssid	   = p[Dot11Elt].info
			bssid	  = p[Dot11].addr3	
			channel = 'n/a'
			# if len(p[Dot11Elt:3].info) == 1:
			# print(p[Dot11Elt:3].ID)
			if p[Dot11Elt:3].ID == 3:
				# print("EEEEEEEEEEEEEEEEHI")
				channel	= int( ord(p[Dot11Elt:3].info))
			capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
					{Dot11ProbeResp:%Dot11ProbeResp.cap%}")

			type_ = Enum_Type.type_packet[p[Dot11].type]
			subtype = Enum_Type.subtypes_management[p[Dot11].subtype]

			signal_decoded = ord(p.notdecoded[-2:-1])
			#info = p.sprintf("802.11 %Dot11.type% %Dot11.subtype% %RadioTap.dBm_AntSignal% %Dot11.pw-mgt% %Dot11.addr2% > %Dot11.addr1%")
			packet_signal = -(256 - signal_decoded) 
			
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
				if signal_decoded > 0:
					self.DB_Man.update_signal_AP(packet_signal, bssid)
				if channel != 'n/a':
					self.DB_Man.update_channel_AP(channel, bssid)
					#TODO Magari se si verificano entrambe, fare solo un metodo
		#print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])

		#if p.haslayer(Dot11):
			#All packets
			# addr1 = p[Dot11].addr1
			# addr2 = p[Dot11].addr2
			# addr3 = p[Dot11].addr3
		try:
			channel	= int( ord(p[Dot11Elt:3].info)) if p.haslayer(Dot11Elt) else 'n/a'
		except:	
			channel = 'n/a'
		capability = p.sprintf("{Dot11ProbeResp:%Dot11ProbeResp.cap%}") if p.haslayer(Dot11ProbeResp) else 'n/a'
		#print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])
		type_ = Enum_Type.type_packet[p[Dot11].type]
		#print(p[Dot11].subtype)
		subtype = Enum_Type.subtypes_management[p[Dot11].subtype]
		signal_decoded = None
		signal_decoded = ord(p.notdecoded[-2:-1]) if hasattr(p, 'notdecoded') else 'n/a'
		#info = p.sprintf("802.11 %Dot11.type% %Dot11.subtype% %RadioTap.dBm_AntSignal% %Dot11.pw-mgt% %Dot11.addr2% > %Dot11.addr1%")
		packet_signal = -(256 - signal_decoded) if signal_decoded != None else 'n/a'

		if hasattr(p, 'FCfield') and p.FCfield is not None:
			DS = p.FCfield & 0x3
			to_DS = DS & 0x1 != 0
			from_DS = DS & 0x2 != 0

		if to_DS and not from_DS:
			BSSID = p[Dot11].addr1
			source = p[Dot11].addr2
			destination = p[Dot11].addr3
		elif not to_DS and from_DS:
			BSSID = p[Dot11].addr2
			destination = p[Dot11].addr1
			source = p[Dot11].addr3
		elif not to_DS and not from_DS:
			destination = p[Dot11].addr1
			source = p[Dot11].addr2
			BSSID = p[Dot11].addr3

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
			# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
			# print(type_packet[p[Dot11].type], " ",subtypes_management[p[Dot11].subtype])
			# print(p.addr1, " ", p.addr2, " ", p.addr3)
			# print(to_DS, " ", from_DS)
			# p.show()
			# #if p.haslayer(EAP_PEAP):
			# print("PEAP: ",p[EAP].type, " ", p[EAP].code)
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


# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# ('Data', ' ', 'Beacon')
# ('fc:19:10:45:ef:01', ' ', 'd8:84:66:43:2a:48', ' ', 'd8:84:66:43:2a:48')
# (False, ' ', True)
