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

import umit.umpa
import umit.umpa.sniffing
from umit.umpa.protocols import IP, TCP
from tests.utils import SendPacket

class TestSendOut(object):
    def test_sndout(self):
        packet = umit.umpa.Packet(IP(src="1.2.3.4", dst="67.205.14.183"),
                            TCP(srcport=81, dstport=80))
        th = SendPacket(packet)
        th.start()
        received = umit.umpa.sniffing.sniff_next(filter="dst 67.205.14.183",
                                            device="any")
        th.join()

        assert received.ip.src == packet.ip.src
        assert received.ip.dst == packet.ip.dst
        assert received.tcp.srcport == packet.tcp.srcport
        assert received.tcp.dstport == packet.tcp.dstport
