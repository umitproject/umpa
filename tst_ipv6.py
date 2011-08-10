#!/usr/bin/env python

from umit.umpa.protocols import IPV6
from umit.umpa.protocols import TCP
from umit.umpa.protocols import UDP
from umit.umpa.protocols import ICMPV6
from umit.umpa.protocols import Payload
from umit.umpa import Packet
from umit.umpa import Socket
from umit.umpa._sockets import INET6
from umit.umpa.utils.security import super_priviliges


ip = IPV6(src='0000:0000:0000:0000:0000:0000:0000:0001', dst='0000:0000:0000:0000:0000:0000:0000:0001')
#ip.set_flags('ds',ect=True)
#ip.set_flags('ds',ecn_ce=True)
#print "Value Of fielf key for Ipv6 is Here"
#print(ip)
#print(list(ip.get_fields_keys()))
#print "______________________________"
#print ICMPV6(type='ECHO')
#tcp = TCP()
#tcp.srcport = 2561
#tcp.dstport = 253
#tcp.set_flags('flags', syn=True)
#tcp._checksum = 38211
#tcp.set_flags('flags', ack=True)
#payload = Payload()
#payload.data = "this is umpa!"
#first_packet = Packet(ip, tcp)
#first_packet.include(payload)
#print "Structure Of Ipv6 Packet"

#print first_packet
#print "_____________________"
sock = super_priviliges(INET6)
#sock.send(first_packet)
#udp = UDP(srcport=263, dstport=153)
#second_packet = Packet(ip, udp)
#print second_packet
#sock.send(second_packet)
icmp = ICMPV6(type = 134 , code = 0)
#icmp.data = '00:00:00:00:00:00'
second_packet = Packet(ip, icmp)
print second_packet
sock.send(second_packet)





