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

from umit.umpa.protocols import IP, UDP, Payload

class TestUDP(object):
    # this tests pre/post raw methods as well
    def test_get_raw(self):
        ip = IP(src='1.2.3.4', dst='5.6.7.8')
        udp = UDP(srcport=9, dstport=10)

        assert udp._raw(0, 0, [ip, udp], 0) == (0x9000A0008EFB7, 64)

    # test length and checksum calculation
    def test_get_raw_with_payload(self):
        ip = IP(src='1.2.3.4', dst='5.6.7.8')
        udp = UDP(srcport=9, dstport=10)
        payload = Payload('12345678')

        # the next two lines are normally done by Packet.get_raw()
        payload.get_raw([ip, udp, payload], 8*len(payload.data))
        udp.__dict__['payload'] = payload

        assert udp._raw(0, 0, [ip, udp, payload], 8*len(payload.data)) == \
                                                       (0x9000a00101ed3L, 64)
