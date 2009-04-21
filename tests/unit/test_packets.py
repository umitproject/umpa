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

from umpa import Packet
from umpa.protocols import IP, TCP, UDP, Payload
from umpa.utils.exceptions import UMPAException, UMPAStrictException
from umpa._packets import StrictWarning

import py.test

class TestUMPAPacketsBasic(object):
    def test_default_options(self):
        p = Packet()
        assert p.strict is True
        assert p.warn is True

    def test_overwrite_options(self):
        p = Packet(strict=False, warn=True)
        assert p.strict is False
        assert p.warn is True

    def test_broken_options(self):
        py.test.raises(UMPAException, Packet, foo=False)
        py.test.raises(UMPAException, Packet, strict=True, foo=False, bar=True)

class TestUMPAPackets(object):
    def test_add_new_protocols__strict(self):
        py.test.raises(UMPAStrictException, Packet, TCP(), IP())
        py.test.raises(UMPAStrictException, Packet, TCP(), IP(), strict=True)
        py.test.raises(UMPAStrictException, Packet, TCP(), Payload(), IP())
        py.test.raises(UMPAStrictException, Packet, TCP(),  IP(), Payload())
        py.test.raises(UMPAStrictException, Packet, Payload(), TCP())
        py.test.raises(UMPAStrictException, Packet, Payload(), TCP())
        py.test.raises(UMPAStrictException, Packet, UDP(), TCP())

        p = Packet(TCP())
        py.test.raises(UMPAStrictException, p.include, IP())
        py.test.raises(UMPAStrictException, p.include, UDP())

        p = Packet(strict=False)
        p.strict = True 
        py.test.raises(UMPAStrictException, p.include, UDP(), TCP())

    def test_add_new_protocols__warn(self):
        # TODO: how py.test handles with warnings?
        py.test.skip('how py.test handles with warnings?')
        p = Packet(strict=False)
        py.test.raises(StrictWarning, "p.include(TCP(), IP())")

    def test_protos_order(self):
        order = (IP, UDP, Payload)

        p = Packet(*[x() for x in order])
        for i in xrange(len(order)):
            assert isinstance(p.protos[i], order[i])

        p = Packet(IP())
        p.include(UDP(), Payload())
        for i in xrange(len(order)):
            assert isinstance(p.protos[i], order[i])

class TestUMPAPacketsOutput(object):
    def setup_class(cls):
        py.test.skip("these tests need more improvemtns. "
                    "propably something is broken also.")

    def test_get_raw__ip(self):
        p = Packet()
        p.include(IP(source_address="127.0.0.1",
                    destination_address="127.0.0.1",
                    _identification=1000,
                    _header_checksum=0x7900))

        assert ("\x45\x00\x00\x14\x55\x8b\x00\x00"
                "\x40\x00\x27\x5d\x7f\x00\x00\x01"
                "\x7f\x00\x00\x01") == p.get_raw()

    def test_get_raw__tcp(self):
        p = Packet()
        p.include(TCP(source_port=0, destination_port=80))

        assert ("\x7f\x00\x00\x01\x00\x00\x00\x50"
                "\x00\x00\x00\x00\x00\x00\x00\x01"
                "\x50\x00\x02\x00\xaf\x91\x00\x00") == p.get_raw()

    def test_get_raw(self):
        p = Packet()
        p.include(IP(source_address="127.0.0.1",
                    destination_address="127.0.0.1"))
        p.include(TCP(source_port=0, destination_port=80))

        assert ("\x45\x00\x00\x28\x00\x00\x00\x00"
                "\x40\x06\xc0\x49\x7f\x00\x00\x01"
                "\x7f\x00\x00\x01\x00\x00\x00\x50"
                "\x00\x00\x00\x00\x00\x00\x00\x01"
                "\x50\x00\x02\x00\xaf\x91\x00\x00") == p.get_raw()

        p.include(Payload("test"))

