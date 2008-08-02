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
from umpa.protocols import IP#, TCP

# create new IP object
ip1 = IP.IP()
# setting some fields
ip1.source_address = "127.0.0.1"
ip1.destination_address = "156.17.17.157"

# the same for TCP
#tcp1 = TCP()
#tcp1.src_port = 6544
#tcp1.dst_port = 9494

# also, SYN flag will be set up
#tcp1.set_flags(syn=True)

# create a new packet and include one protocol (ip1)
packet = umpa.Packet(ip1)
# packing another protocol into our packet
#packet.include(tcp1)

# creating new socket connection
sock = umpa.Socket()

# sending packet
sock.send(packet)
