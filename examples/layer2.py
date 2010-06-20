#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Adriano Monteiro Marques.
#
# Author: Kosma Moczek <kosma at kosma dot pl>
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

"""
This example shows how to send raw Ethernet frames using SocketL2 class.
"""

import umit.umpa
import umit.umpa.utils.security

from umit.umpa.protocols import Ethernet, IP, UDP, Payload
from umit.umpa import SocketL2, Packet

# Create a raw Ethernet socket. The 'iface' argument is mandatory.
sock = umit.umpa.SocketL2(iface='eth0')

# Drop root privileges after socket creation. This improves security.
umit.umpa.utils.security.drop_priviliges()

# Create protocol objects. We need to specify MAC addresses since we operate
# on the link layer.
ethernet = Ethernet(src='00:11:22:33:44:55', dst='01:23:45:67:89:AB')
ip = IP(src='192.168.1.234', dst='192.168.1.1')
udp = UDP(srcport=1234, dstport=4321)
payload = Payload("UMPA")

# Create a new Packet object.
packet = Packet(ethernet, ip, udp, payload)

# Send the packet. Use a network sniffer (e.g. Wireshark) to see it.
sock.send(packet)
