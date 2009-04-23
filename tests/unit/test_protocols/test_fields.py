#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
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

import py.test
from umpa.protocols._fields import *
from umpa.utils.exceptions import UMPAException, UMPAAttributeException

class TestField(object):
    cls_field = Field

    def test_init(self):
        f = self.cls_field('foobar')
        assert f.auto is False

    def test_set(self):
        f = self.cls_field('foobar')
        py.test.raises(NotImplementedError, f.set, 0)

    def test_get(self):
        f = self.cls_field('foobar', 10)
        assert f.get() == 10
        
        f = self.cls_field('foobar')
        assert f.get() is None

    def test_clear(self):
        f = self.cls_field('foobar', 10)
        f.clear()
        assert f.get() is None
    
    def test_doc(self):
        f = self.cls_field('foobar')
        f.set_doc('xxx')
        assert f.__doc__ == 'xxx'

    def test_fillout(self):
        f = self.cls_field('foobar')
        py.test.raises(UMPAException, f.fillout)

        f = self.cls_field('foobar', 10)
        py.test.raises(NotImplementedError, f.fillout)

    def test_raw_value(self):
        f = self.cls_field('foobar')
        py.test.raises(NotImplementedError, f._raw_value)

class TestIntField(TestField):
    cls_field = IntField

    def test_raw_value(self):
        f = self.cls_field('foobar', 10)
        assert f._raw_value() == 10

    def test_set(self): #_is_valid() tests included
        f = self.cls_field('foobar', 10, 5)
        assert f.get() == 10

        f = self.cls_field('foobar', bits=5)
        f.set(10)
        assert f.get() == 10

        f = self.cls_field('foobar', bits=4)
        f.set(10)
        assert f.get() == 10

        f = self.cls_field('foobar', bits=3)
        py.test.raises(UMPAAttributeException, f.set, 10)

    def test_fillout(self):
        f = self.cls_field('foobar')
        py.test.raises(UMPAException, f.fillout)

        f = self.cls_field('foobar', 10)
        assert f.fillout() == 10

class TestSpecialIntField(TestIntField):
    cls_field = SpecialIntField

    def test_tmpvalue(self):
        f = self.cls_field('foobar')
        
        assert f.get_tmpvalue() == 0
        assert f._tmp_value == 0

        f.set_tmpvalue(10)
        assert f.get_tmpvalue() == 10

        f.clear_tmpvalue()
        assert f._tmp_value == 0

        f._tmp_value = 20
        assert f._tmp_value == 20

        del f._tmp_value
        assert f.get_tmpvalue() == 0

class TestEnumField(TestIntField):
    cls_field = EnumField

    def test_get(self):
        f = self.cls_field('foobar', 10, 16)
        f.enumerable = {'foo' : 5, 'bar' : 10}

        assert f.get() == 10
        assert f.get(True) == 'bar'

        f.set(5)
        assert f.get(human=True) == 'foo'

        f.set(0)
        assert f.get(True) == 0

    def test_set(self):
        f = self.cls_field('foobar', bits=16)
        f.enumerable = {'foo' : 5, 'bar' : 10}

        f.set('foo')
        assert f.get() == 5
        assert f.get(True) == 'foo'

        f.set(10)
        assert f.get() == 10
        assert f.get(True) == 'bar'

class TestAddrField(TestField):
    pass

class TestIPAddrField(TestAddrField):
    cls_field = IPAddrField

    def test_set(self):
        f = self.cls_field('foobar')

        def check(val):
            f.set(val)
            assert f.get() == val

        f.pieces_amount = 4
        f.separator = "."
        f.piece_size = 8
        f.base = 10

        check("255.255.255.255")
        check((255,255,255,255))
        check("127.0.0.1")
        check("0.0.0.0")
        check((127,0,0,1))
        check((0,0,0,0))
        f.set([127,0,0,1])
        assert f.get() == (127,0,0,1)
        f.set([0,0,0,0])
        assert f.get() == (0,0,0,0)

        py.test.raises(UMPAAttributeException, f.set, "256.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "127,0,0,1")
        py.test.raises(UMPAAttributeException, f.set, "327,0,0,1")
        py.test.raises(UMPAAttributeException, f.set, "127.0.0.")
        py.test.raises(UMPAAttributeException, f.set, "127")
        py.test.raises(UMPAAttributeException, f.set, "A")
        py.test.raises(UMPAAttributeException, f.set, "0xF.0xF.0xF.0xF")
        py.test.raises(UMPAAttributeException, f.set, (500,))
        py.test.raises(UMPAAttributeException, f.set, (500,0,0,0))
        py.test.raises(UMPAAttributeException, f.set, ("10.0.0.0",))

        f.separator = "*"
        check("127*0*0*1")
        py.test.raises(UMPAAttributeException, f.set, "127.0.0.1")

        f.pieces_amount = 3
        check("127*0*1")
        py.test.raises(UMPAAttributeException, f.set, "127.0.0.1")

        f.pieces_amount = 4
        f.separator = "."
        f.piece_size = 6
        check("63.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "127.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "65.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "64.0.0.1")

        f.piece_size = 8
        f.base = 16
        check("0xFF.0xFF.0xFF.0xFF")
        py.test.raises(UMPAAttributeException, f.set, "0xG.0xFF.0xFF.0xFF")

    def test_raw_value(self):
        f = self.cls_field('foobar')
        f.pieces_amount = 4
        f.separator = "."
        f.piece_size = 8
        f.base = 10

        f.set("127.0.0.1")
        assert f._raw_value() == 2130706433
        f.set("0.0.0.0")
        assert f._raw_value() == 0
        f.set("255.255.255.255")
        assert f._raw_value() == 2**32-1

    def test_fillout(self):
        f = self.cls_field('foobar')
        py.test.raises(UMPAException, f.fillout)

        f.pieces_amount = 4
        f.separator = "."
        f.piece_size = 8
        f.base = 10

        f.set("127.0.0.1")
        assert f.fillout() == 2130706433
        f.set("0.0.0.0")
        assert f.fillout() == 0
        f.set("255.255.255.255")
        assert f.fillout() == 2**32-1

class TestIPv4AddrField(TestIPAddrField):
    cls_field = IPv4AddrField

    def test_set(self):
        f = self.cls_field('foobar')

        def check(val):
            f.set(val)
            assert f.get() == val

        check("127.0.0.1")
        check("0.0.0.0")
        check((127,0,0,1))
        check((0,0,0,0))
        f.set([127,0,0,1])
        assert f.get() == (127,0,0,1)
        f.set([0,0,0,0])
        assert f.get() == (0,0,0,0)

        py.test.raises(UMPAAttributeException, f.set, "256.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "127,0,0,1")
        py.test.raises(UMPAAttributeException, f.set, "327,0,0,1")
        py.test.raises(UMPAAttributeException, f.set, "127.0.0.")
        py.test.raises(UMPAAttributeException, f.set, "127")
        py.test.raises(UMPAAttributeException, f.set, "A")
        py.test.raises(UMPAAttributeException, f.set, "0xF.0xF.0xF.0xF")
        py.test.raises(UMPAAttributeException, f.set, (500,))
        py.test.raises(UMPAAttributeException, f.set, (500,0,0,0))
        py.test.raises(UMPAAttributeException, f.set, ("10.0.0.0",))

class TestIPv6AddrField(TestIPAddrField):
    cls_field = IPv6AddrField

    def test_set(self):
        f = self.cls_field('foobar')

        def check(val):
            f.set(val)
            assert f.get() == val

        check("0:0:0:0:0:0:0:0")
        check("FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF")
        check("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        check((0,0,0,0,0,0,0,0))
        check((0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF))
        check((0x2001,0x0db8,0x85a3,0,0,0x8a2e,0x0370,0x7334))
        f.set([0,0,0,0,0,0,0,0])
        assert f.get() == (0,0,0,0,0,0,0,0)
        f.set([0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF])
        assert f.get() == (0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,
                                                                        0xFFFF)
        f.set([0x2001,0x0db8,0x85a3,0,0,0x8a2e,0x0370,0x7334])
        assert f.get() == (0x2001,0x0db8,0x85a3,0,0,0x8a2e,0x0370,0x7334)

        py.test.raises(UMPAAttributeException, f.set, "127.0.0.1")
        py.test.raises(UMPAAttributeException, f.set, "FFFF.FFFF.FFFF.FFFF")
        py.test.raises(UMPAAttributeException, f.set,
                                    "FFFF.FFFF.FFFF.FFFF.FFFF.FFFF.FFFF.FFFF")
        py.test.raises(UMPAAttributeException, f.set, "G:G:G:G:G:G:G:G")
