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

from umit.umpa.protocols import ARP

class TestARP(object):
    def test_get_raw(self):
        arp = ARP(opcode="REQUEST", srchw_mac="aa:bb:cc:dd:ee:ff")
        assert arp._raw(0, 0, [arp], 0) == (0x0001080006040001aabbccddeeff7f0000010000000000007f000001, 224)

        arp = ARP(opcode="REPLY", dsthw_mac="aa:bb:cc:dd:ee:ff",
                prototype=0x1234)
        assert arp._raw(0, 0, [arp], 0) == (0x00011234060000020000000000007f000001aabbccddeeff7f000001, 224)
