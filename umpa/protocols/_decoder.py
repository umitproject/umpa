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

import umpa
from umpa.protocols import Ethernet, IP, TCP, UDP, Payload
from umpa.protocols import _consts as consts

def decode(buffer, linktype):
    # TODO: rewrite to check what protocols are available (also local from $HOME)
    # and keep it in a dict
    # XXX propably type of upper layer should be unified
    packet = umpa.Packet()

    # 2nd layer
    next_type = None
    if linktype == consts.DLT_EN10MB:
        header = Ethernet()
        buffer = header.load_raw(buffer)
        next_type = header._type
    #elif linktype == consts.DLT_LINUX_SLL:
    #    raise Exception("got SLL")
    #    header = SLL()
    #    header.load_raw(buffer)
    #    next_type = header.ltype
    else:
        header = Payload()
        header.load_raw(buffer)
        packet.include(header)
        return packet
    packet.include(header)

    # 3rd layer
    if next_type == consts.ETHERTYPE_IP:
        header = IP()
        buffer = header.load_raw(buffer)
        next_type = header._proto
    #elif next_type == consts.ETHERTYPE_IPV6:
    #    header = IPv6()
    #    header.load_raw(buffer)
    #    next_type = header.nxt
    else:
        header = Payload()
        header.load_raw(buffer)
        packet.include(header)
        return packet
    packet.include(header)

    # 4th layer
    if next_type == consts.PROTOCOL_TCP:
        header = TCP()
        buffer = header.load_raw(buffer)
    elif next_type == consts.PROTOCOL_UDP:
        header = UDP()
        buffer = header.load_raw(buffer)
    else:
        header = Payload()
        header.load_raw(buffer)
        packet.include(header)
        return packet
    packet.include(header)

    # payload
    data = Payload()
    data.load_raw(buffer)
    packet.include(data)

    return packet
