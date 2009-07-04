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

from umpa.protocols import TCP, IP, Payload

class TestTCP(object):
    def test_get_raw(self):
        # TODO more tests would be nice
        # this test pre/post raw methods as well
        ip = IP(src='127.0.0.1', dst='127.0.0.1')
        tcp = TCP(srcport=0, dstport=10)

        assert tcp._raw(0, 0, [ip, tcp], 0) == \
                (0xa000000000000000150000200afd70000, 160)


        # XXX can't test it because it's vary on umpa.Packet
        #payload = Payload('test')
        #tcp.__dict__['payload'] = payload
        #print tcp._raw(0, 0, [ip, tcp, payload], 0)
        #assert tcp._raw(0, 0, [ip, tcp, payload], 0) == \
        #        (0xa000000000000000150000200c7f90000, 192)
