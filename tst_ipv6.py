#!/usr/bin/env python

from umit.umpa.protocols import IPV6
from umit.umpa.protocols import TCP6
from umit.umpa.protocols import UDP6
from umit.umpa.protocols import Payload
from umit.umpa import Packet
from umit.umpa import Socket
from umit.umpa._sockets import INET6
from umit.umpa.utils.security import super_priviliges


ip = IPV6(src='0:0:0:0:0:0:0:1', dst='0:0:0:0:0:0:0:1')
print "Value Of fielf key for Ipv6 is Here"
print(ip)
print(list(ip.get_fields_keys()))
print "______________________________"

tcp = TCP6()
tcp.srcport = 2958
tcp.dstport = 0
tcp.set_flags('flags', syn=True)
payload = Payload()
payload.data = "this is umpa!"
first_packet = Packet(ip, tcp)
first_packet.include(payload)
print "Structure Of Ipv6 Packet"

print first_packet
print "_____________________"
sock = super_priviliges(INET6)
sock.send(first_packet)

print "Test for UDP protcol"
udp = UDP6(srcport=0, dstport=7)
print(ip.get_field("_nxt_hdr").enumerable)
ip._nxt_hdr = "UDP"
second_packet = Packet(ip, udp)
print second_packet
sock.send(second_packet)

