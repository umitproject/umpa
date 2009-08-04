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

from umit.umpa.protocols import Ethernet

class TestEthernet(object):
    def test_get_raw(self):
        eth = Ethernet(src="aa:bb:cc:dd:ee:ff")
        assert eth._raw(0, 0, [eth], 0) == (0x000000000000aabbccddeeff0000,112)

        eth = Ethernet( dst="ff:ff:ff:00:00:00",
                        src="aa:bb:cc:dd:ee:ff",
                        _type=0xffff)
        assert eth._raw(0, 0, [eth], 0) == (0xffffff000000aabbccddeeffffff,112)
