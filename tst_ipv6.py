#!/usr/bin/env python

from umit.umpa.protocols import IPV6
from umit.umpa.protocols import TCP
from umit.umpa.protocols import UDP
from umit.umpa.protocols import ICMP
from umit.umpa.protocols import ICMPV6
from umit.umpa.protocols import Payload
from umit.umpa import Packet
from umit.umpa import Socket
from umit.umpa._sockets import INET6
from umit.umpa.utils.security import super_priviliges


ip = IPV6(src='0000:0000:0000:0000:0000:0000:0000:0001', dst='0000:0000:0000:0000:0000:0000:0000:0001')

def raw(obj):
    return obj._raw(0, 0, [obj], 0)
    
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
icmp = ICMPV6(type = 137 , code = 0)
#icmp.data = '00:00:00:00:00:00'
#icmp.ident = 4660
#icmp.seq = 22136
icmp.data = 'ABCD'
second_packet = Packet(ip, icmp)
print second_packet
sock.send(second_packet)
#i = IPV6()
#i.load_raw("\x88\x00\x92\x84\xB2\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12\x92\x84\x12\xB4\x56\xB4\x56\x78\x80\x04\x16\x28\x03\x06\x84\x12\x02\x84\x14\xB4\x53\xB4\x56\x78")
#print i._version
#print i.dscp
#print i.ds
#print i._flow_label
#print i._payload
#print i._nxt_hdr
#print i._hop_limit
#print i.src
#print i.dst


#########################################################













