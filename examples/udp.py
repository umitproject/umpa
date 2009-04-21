#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
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

# this example shows how to send UDP datagrams

import umpa
import umpa.utils.security

from umpa.protocols import IP, UDP

# NOTE:
# to create RAW_SOCKET we need SUID, but for normal usage it's not
# necessary. we recommend to use umpa.utils.security to make our programs
# more safety. also dropping priviliges should be done at the same beginning
# of the application

# dropping unnecessary priviliges
umpa.utils.security.drop_priviliges()

# create new IP object
ip = IP()
# setting some fields
ip.source_address = "127.0.0.1"
ip.destination_address = "67.205.14.183"

# create new UDP object
udp = UDP()
# setting some fields
udp.source_port = 0
udp.destination_port = 7

# create a new packet and include protocols
packet = umpa.Packet(ip, udp)

# creating new socket connection
# NOTE: we need to raise our priviliges.
# we can call super_priviliges() function and pass function which need these
# priviliges as an argument. after that, we drop priviliges automatically

# we can do the same with the code:
# umpa.utils.security.super_priviliges()
# sock = umpa.Socket()
# umpa.utils.security.drop_priviliges()

sock = umpa.utils.security.super_priviliges(umpa.Socket)

# sending packet
sock.send(packet)
