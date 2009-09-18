#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This library is free software; you can redistribute it and/or modify 
# it under the terms of the GNU Lesser General Public License as published 
# by the Free Software Foundation; either version 2.1 of the License, or 
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public 
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License 
# along with this library; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 

# this example shows how to send broken packets with not saved layers order

import time
import threading

import umit.umpa
import umit.umpa.sniffing
from umit.umpa.protocols import IP, TCP, Payload

# prepare packet which we want to sniff
# to get possibility of sniffing and sending packets at the same
# we use threads where after a small delay we send a packet
#
# obviously it's not necessary in real usecase
class SendPacket(threading.Thread):
    def __init__(self, packet, amount=1):
        super(SendPacket, self).__init__()
        self._packet = packet
        self._amount = amount
    def run(self):
        print "Sending %d packets..." % self._amount
        s = umit.umpa.Socket()
        for i in xrange(self._amount):
            time.sleep(2)
            s.send(self._packet)

packet = umit.umpa.Packet(IP(src="1.2.3.4", dst="127.0.0.1"),
                    TCP(srcport=99), Payload(data="sniff me"))

# run thread and send packet
th = SendPacket(packet)
th.start()

# sniff packet
#
# we set a filter to capture expected packet
# (see BPF documentation for more information)
#
# arguments:
# number of sniffed packets - 1
# filter - BPF filter
# device - interface where we want to capture packets
#
# NOTE: if we are interested only with 1 packet,
#       we can call sniff_next() instead of sniff()
#       returning object will be umpa.Packet not list of umpa.Packet then
received_packets = umit.umpa.sniffing.sniff(1, filter="src 1.2.3.4 and port 99",
                                                                device="any")

# collect terminated thread
th.join()

# print sniffed packet
print "Captured %d packets:" % len(received_packets)
print received_packets[0]

print "\n_____________________"
# the same but send and receive 2 packets
th = SendPacket(packet, 2)
th.start()
received_packets = umit.umpa.sniffing.sniff(2, filter="src 1.2.3.4 and port 99",
                                                                device="any")
th.join()
print "Captured %d packets:" % len(received_packets)
for pkt in received_packets:
    print pkt

print "\n_____________________"
# using callbacks
def cbk(ts, pkt, *args):
    print "[%f] Captured a new packet.." % ts
    print pkt

th = SendPacket(packet, 2)
th.start()
umit.umpa.sniffing.sniff_loop(2, filter="src 1.2.3.4 and port 99",
                                    device="any", callback=cbk)
th.join()
