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

import sys
from umit.umpa import Packet
from umit.umpa.protocols import Ethernet, IP, TCP, UDP, Payload
from umit.umpa.protocols import _consts
from umit.umpa.utils.exceptions import UMPAException, UMPAStrictException, \
                                       UMPAAttributeException
from umit.umpa._packets import StrictWarning

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

    def test_proto_access(self):
        p = Packet(IP(), TCP())
        assert isinstance(p.protos[0], IP)
        assert isinstance(p.protos[1], TCP)
        assert isinstance(p.ip, IP)
        assert isinstance(p.tcp, TCP)

    def test_proto_access_edit(self):
        p = Packet(IP(src="1.2.3.4"), TCP())
        assert p.ip.src == "1.2.3.4"
        p.ip.src = "10.0.0.1"
        assert p.ip.src == "10.0.0.1"

        ip = IP(src="127.0.0.1")
        p = Packet(ip)
        p.ip.src = "10.0.0.1"
        assert p.ip.src == "10.0.0.1"
        assert ip.src == "10.0.0.1"

class TestUMPAPackets(object):
    def test_add_new_protocols__strict(self):
        py.test.raises(UMPAStrictException, Packet, TCP(), IP())
        py.test.raises(UMPAStrictException, Packet, TCP(), IP(), strict=True)
        py.test.raises(UMPAStrictException, Packet, TCP(), Payload(), IP())
        py.test.raises(UMPAStrictException, Packet, TCP(),  IP(), Payload())
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

    def test_get_destination(self):
        p = Packet(Ethernet(dst='00:11:22:33:44:55'),
                   IP(dst='1.2.3.4'),
                   UDP(dstport=1234),
                   Payload('UMPA'))
        
        py.test.raises(UMPAException, p._get_destination, 1);
        assert p._get_destination(2) == '00:11:22:33:44:55'
        assert p._get_destination(3) == '1.2.3.4'
        py.test.raises(UMPAAttributeException, p._get_destination, 4);
        py.test.raises(UMPAAttributeException, p._get_destination, 5);
        py.test.raises(UMPAException, p._get_destination, 6);

class TestUMPAPacketsOutput(object):
    def test_get_raw__ip(self):
        p = Packet()
        p.include(IP(src="127.0.0.1",
                    dst="127.0.0.1",
                    _id=1000,
                    _checksum=0x7900))

        if sys.platform.find('linux') != -1:
            ttl = _consts.TTL_LINUX
        elif sys.platform.find('darwin') != -1:
            ttl = _consts.TTL_MACOS
        elif sys.platform.find('win') != -1:
            ttl = _consts.TTL_WINDOWS
        elif sys.platform.find('freebsd') != -1:
            ttl = _consts.TTL_FREEBSD
        elif sys.platform.find('os2') != -1:
            ttl = _consts.TTL_OS2
        elif sys.platform.find('sunos') != -1:
            ttl = _consts.TTL_SUNOS
        elif sys.platform.find('aix') != -1:
            ttl = _consts.TTL_AIX
        elif sys.platform.find('irix') != -1:
            ttl = _consts.TTL_IRIX
        elif sys.platform.find('solaris') != -1:
            ttl = _consts.TTL_SOLARIS
        elif sys.platform.find('ultrix') != -1:
            ttl = _consts.TTL_ULTRIX
        elif sys.platform.find('dec') != -1:
            ttl = _consts.TTL_DEC
        else:
            ttl = _consts.TTL_LINUX

        expected = ("\x45\x00\x00\x14\x03\xe8\x00\x00"
                    "%c\x00\x79\x00\x7f\x00\x00\x01"
                    "\x7f\x00\x00\x01") % chr(ttl)
        assert expected == p.get_raw()

    def test_get_raw__tcp(self):
        p = Packet()
        p.include(TCP(srcport=123,dstport=321,flags='psh'))

        assert ("\x00\x7b\x01\x41\x00\x00\x00\x00"
                "\x00\x00\x00\x01\x50\x08\x02\x00"
                "\xae\x1d\x00\x00") == p.get_raw()

    def test_get_raw(self):
        if sys.platform.find('linux') != -1:
            ttl = _consts.TTL_LINUX
        elif sys.platform.find('darwin') != -1:
            ttl = _consts.TTL_MACOS
        elif sys.platform.find('win') != -1:
            ttl = _consts.TTL_WINDOWS
        elif sys.platform.find('freebsd') != -1:
            ttl = _consts.TTL_FREEBSD
        elif sys.platform.find('os2') != -1:
            ttl = _consts.TTL_OS2
        elif sys.platform.find('sunos') != -1:
            ttl = _consts.TTL_SUNOS
        elif sys.platform.find('aix') != -1:
            ttl = _consts.TTL_AIX
        elif sys.platform.find('irix') != -1:
            ttl = _consts.TTL_IRIX
        elif sys.platform.find('solaris') != -1:
            ttl = _consts.TTL_SOLARIS
        elif sys.platform.find('ultrix') != -1:
            ttl = _consts.TTL_ULTRIX
        elif sys.platform.find('dec') != -1:
            ttl = _consts.TTL_DEC
        else:
            ttl = _consts.TTL_LINUX

        expected = ("\x45\x00\x00\x28\x03\xe8\x00\x00"
                    "%c\x06\x79\x00\x7f\x00\x00\x01"
                    "\x7f\x00\x00\x01") % chr(ttl)

        p = Packet()
        p.include(IP(src="127.0.0.1",
                    dst="127.0.0.1",
                    _id=1000,
                    _checksum=0x7900))
        p.include(TCP(srcport=123, dstport=321, flags='psh'))

        expected += ("\x00\x7b\x01\x41\x00\x00\x00\x00"
                    "\x00\x00\x00\x01\x50\x08\x02\x00"
                    "\xae\x1d\x00\x00")
        assert expected == p.get_raw()

        p.include(Payload(data="UMPA"))

        expected = ("\x45\x00\x00\x2c\x03\xe8\x00\x00"
                    "%c\x06\x79\x00\x7f\x00\x00\x01"
                    "\x7f\x00\x00\x01"
                    "\x00\x7b\x01\x41\x00\x00\x00\x00"
                    "\x00\x00\x00\x01\x50\x08\x02\x00"
                    "\x08\x8b\x00\x00") % chr(ttl)

        expected += "\x55\x4d\x50\x41"
        assert expected == p.get_raw()
