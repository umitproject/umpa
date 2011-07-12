#!/usr/bin/env python

from umit.umpa.protocols import IP
from umit.umpa.protocols import TCP
from umit.umpa.protocols import UDP
from umit.umpa.protocols import Payload
from umit.umpa import Packet
from umit.umpa import Socket
from umit.umpa._sockets import INET
from umit.umpa.utils.security import super_priviliges


ip = IP(src='127.0.0.1', dst='127.0.0.1')
print "Value Of fielf key for Ipv6 is Here"
print(ip)
print(list(ip.get_fields_keys()))
print "______________________________"

tcp = TCP()
tcp.srcport = 2952
tcp.dstport = 2554
tcp.set_flags('flags', syn=True)
payload = Payload()
payload.data = "this is umpa!"
first_packet = Packet(ip, tcp)
first_packet.include(payload)
print "Structure Of Ipv4 Packet"

print first_packet
print "_____________________"
sock = super_priviliges(INET)
sock.send(first_packet)


