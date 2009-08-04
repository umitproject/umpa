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

import os.path

from umit.umpa.protocols._decoder import decode
from umit.umpa.protocols import _consts
import tests.a_unit.test_protocols

class TestDecode(object):
    def test_iface_any(self):
        # for some reasons CWD is set to /tmp
        path = os.path.dirname(tests.a_unit.test_protocols.__file__)
        buf = open(os.path.join(path,'any.buf'), 'rb').read()
        pkt = decode(buf, _consts.DLT_LINUX_SLL)

        assert pkt.sll._pkttype == 4
        assert pkt.sll._hatype == 1
        assert pkt.sll._halen == 6
        assert pkt.sll.src == "00:1c:bf:2c:d7:c8"
        assert pkt.sll._blank == 0
        assert pkt.sll._etype == 0x0800

        assert pkt.ip._version == 4
        assert pkt.ip._hdr_len == 0x5
        assert pkt.ip.tos == 0
        assert pkt.ip._len == 0x0028
        assert pkt.ip._id == 0x04a9
        assert pkt.ip.flags == 0
        assert pkt.ip._frag_offset == 0
        assert pkt.ip.ttl == 64
        assert pkt.ip._proto == 0x06
        assert pkt.ip._checksum == 0xe4d1
        assert pkt.ip.src == "192.168.10.108"
        assert pkt.ip.dst == "64.13.134.52"
        
        assert pkt.tcp.srcport == 3001
        assert pkt.tcp.dstport == 0
        assert pkt.tcp._seq == 0x4e885af8
        assert pkt.tcp._ack == 0x2ccc2f2e
        assert pkt.tcp._hdr_len == 0x5
        assert pkt.tcp._reserved == 0
        assert pkt.tcp.flags == 0x02
        assert pkt.tcp._window_size == 512
        assert pkt.tcp._checksum == 0x0b59
        assert pkt.tcp._urgent_pointer == 0

    def test_iface_eth(self):
        # for some reasons CWD is set to /tmp
        path = os.path.dirname(tests.a_unit.test_protocols.__file__)
        buf = open(os.path.join(path,'eth.buf'), 'rb').read()
        pkt = decode(buf, _consts.DLT_EN10MB)

        assert pkt.ethernet.dst == "00:22:b0:84:01:05"
        assert pkt.ethernet.src == "00:1c:bf:2c:d7:c8"
        assert pkt.ethernet._type == 0x0800

        assert pkt.ip._version == 4
        assert pkt.ip._hdr_len == 0x5
        assert pkt.ip.tos == 0
        assert pkt.ip._len == 0x0028
        assert pkt.ip._id == 0x00ce
        assert pkt.ip.flags == 0
        assert pkt.ip._frag_offset == 0
        assert pkt.ip.ttl == 64
        assert pkt.ip._proto == 0x06
        assert pkt.ip._checksum == 0xe8ac
        assert pkt.ip.src == "192.168.10.108"
        assert pkt.ip.dst == "64.13.134.52"
        
        assert pkt.tcp.srcport == 2504
        assert pkt.tcp.dstport == 0
        assert pkt.tcp._seq == 0x45db49ee
        assert pkt.tcp._ack == 0x095cc39b
        assert pkt.tcp._hdr_len == 0x5
        assert pkt.tcp._reserved == 0
        assert pkt.tcp.flags == 0x02
        assert pkt.tcp._window_size == 512
        assert pkt.tcp._checksum == 0xb603
        assert pkt.tcp._urgent_pointer == 0
