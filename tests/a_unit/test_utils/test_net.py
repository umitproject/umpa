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

from umpa.utils.net import *

class TestUtilNet(object):
    def test_in_cksum(self):
        def check(data, cksum):
            assert in_cksum(data) == cksum
            assert in_cksum(data+cksum) == 0
            assert in_cksum(data, cksum) == 0

        for i, j in (
                    (0x0100F203F4F5F6F70000, 0x210E),
                    (0xe34f2396442799f3, 0x1aff),
                    ):
            yield check, i, j
class TestUtilParseIPv4(object):
    def test_parse(self):
        def check(ip, result):
            assert parse_ipv4(ip) == result
            for i in result:
                assert i <=255 
        yield check, "192.168.1.1", [192, 168, 1,1]
        yield check, "255.255.255.0", [255, 255, 255,0]
        yield check, "194.22.11.21", [194, 22, 11,21]
            