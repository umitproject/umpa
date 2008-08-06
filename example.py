#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
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

# This an example of how to use UMPA

import umpa
from umpa.protocols import IP, TCP, UDP

# create new IP object
ip1 = IP.IP()
# setting some fields
ip1.source_address = "127.0.0.1"
#ip1.destination_address = "127.0.0.1"
ip1.destination_address = "67.205.14.183"

# the same for TCP
tcp1 = TCP.TCP()
tcp1.source_port = 2958
tcp1.destination_port = 0

# also, SYN flag will be set up
tcp1.set_flags('control_bits',syn=True,ack=True)

# create a new packet and include one protocol (ip1)
packet = umpa.Packet(ip1)
# packing another protocol into our packet
packet.include(tcp1)

# creating new socket connection
sock = umpa.Socket()

# sending packet
sock.send(packet)


# UDP example
udp1 = UDP.UDP()
udp1.source_port = 0
udp1.destination_port = 7
packet2 = umpa.Packet(ip1, udp1)
sock.send(packet2)
