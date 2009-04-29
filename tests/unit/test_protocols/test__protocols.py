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

import types
import py.test

from umpa.protocols._protocols import Protocol
from umpa.protocols._fields import IntField, Flags
from umpa.utils.exceptions import UMPAException, UMPAAttributeException

class TestProtocol(object):
    def test_init(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        p = Protocol(fake_fields)
        assert p._fields == {}

        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        for i, k in enumerate(fake_ordered):
            assert p._fields[k] == fake_fields[i]

        p = Protocol(fake_fields,a=100)
        assert p.a == 100
        assert p.b == 1
        assert p.c == 1

    def test_getattr(self):
        fake_fields = [IntField('foobar', 1, 8)]
        fake_ordered = ('a')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        
        assert p.a == 1
        py.test.raises(UMPAAttributeException, "p.d")

    def test_setattr(self):
        fake_fields = [IntField('foobar', 1, 8)]
        fake_ordered = ('a')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        p.a = 10
        assert p.a == 10

        py.test.raises(UMPAAttributeException, "p.a = 1000")
        py.test.raises(UMPAAttributeException, "p.b = 1000")
        py.test.raises(UMPAAttributeException, "p.b = 1")

    def test_is_valid(self):
        fake_fields = [IntField('foobar', 1, 8)]
        fake_ordered = ('a')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        
        assert p._is_valid('a')
        assert not p._is_valid('b')
        assert not p._is_valid(None)
        assert not p._is_valid(1)

    def test_get_fields_keys(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        for i, f in enumerate(p.get_fields_keys()):
            assert f == fake_ordered[i]

        assert isinstance(p.get_fields_keys(), types.GeneratorType)

    def test_get_fields(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        for i, f in enumerate(p.get_fields()):
            assert f == fake_fields[i]

        assert isinstance(p.get_fields_keys(), types.GeneratorType)

    def test_get_field(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        for i, f in enumerate(fake_ordered):
            assert p.get_field(f) == fake_fields[i]

    def test_set_fields(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        
        p.set_fields('a', 4, 'b',0)
        assert p.a == 4
        assert p.b == 0
        p.set_fields('a', 10, c=20, b=4)
        assert p.a == 10
        assert p.b == 4
        assert p.c == 20

        py.test.raises(UMPAAttributeException, p.set_fields, 'a', 300)
        py.test.raises(UMPAAttributeException, p.set_fields, 'a', 1, c=300)
        py.test.raises(UMPAAttributeException, p.set_fields, c=300)
        py.test.raises(UMPAAttributeException, p.set_fields, a=1, c=300)

        py.test.raises(UMPAAttributeException, p.set_fields, 'd', 0)
        py.test.raises(UMPAAttributeException, p.set_fields, 'a')

    def test_get_flags(self):
        bits = ['x', 'y', 'z']
        fake_fields = [IntField('foobar', 1, 8), Flags('flags', bits, y=True)]
        fake_ordered = ('a', 'b')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        
        assert p.get_flags('b', 'x', 'y') == [False, True]
        assert p.get_flags('b') == [False, True, False]

        py.test.raises(UMPAAttributeException, p.get_flags, 'a', 'x')
        py.test.raises(UMPAAttributeException, p.get_flags, 'b', 'g')
        py.test.raises(UMPAAttributeException, p.get_flags, 'b', 'x', 'g')

    def test_set_flags(self):
        bits = ['x', 'y', 'z']
        fake_fields = [IntField('foobar', 1, 8), Flags('flags', bits, y=True)]
        fake_ordered = ('a', 'b')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)
        
        p.set_flags('b', 'x', True, 'y', False)
        assert p.get_flags('b') == [True, False, False]
        p.set_flags('b', 'x', True, z=True, y=True)
        assert p.get_flags('b') == [True, True, True]

        py.test.raises(UMPAAttributeException, p.set_flags, 'b', 'x')
        py.test.raises(UMPAAttributeException, p.set_flags, 'a')
        py.test.raises(UMPAAttributeException, p.set_flags, 'a', 'x', True)

    def test_offset(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        assert p.get_offset('a') == 0
        assert p.get_offset('b') == 8
        assert p.get_offset('c') == 16

        fake_fields[1].bits = 10
        assert p.get_offset('a') == 0
        assert p.get_offset('b') == 8
        assert p.get_offset('c') == 18

        assert p.get_offset(fake_fields[0]) == 0
        assert p.get_offset(fake_fields[1]) == 8
        assert p.get_offset(fake_fields[2]) == 18

        fake_fields[1].bits = 8
        assert p.get_offset(fake_fields[0]) == 0
        assert p.get_offset(fake_fields[1]) == 8
        assert p.get_offset(fake_fields[2]) == 16

        py.test.raises(UMPAException, p.get_offset, 10)
        py.test.raises(UMPAException, p.get_offset, Protocol)
        py.test.raises(UMPAException, "p.get_offset(Protocol('x'))")
        py.test.raises(UMPAException, p.get_offset, False)

        py.test.raises(UMPAAttributeException, p.get_offset, 'd')
        py.test.raises(UMPAAttributeException, 'p.get_offset(IntField("x"))')

    def test_pre_raw(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        py.test.raises(NotImplementedError, p._pre_raw, 1, 2, 3, 4)

    def test_post_raw(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        py.test.raises(NotImplementedError, p._post_raw, 1, 2, 3, 4)

    def test_raw(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered
        p = Protocol(fake_fields)

        py.test.raises(NotImplementedError, p._pre_raw, 1, 2, 3, 4)

        old_pre = Protocol._pre_raw
        old_post = Protocol._post_raw
        def fake_fun(*args):
            return args[1], args[2]
        Protocol._pre_raw = fake_fun
        Protocol._post_raw = fake_fun

        p = Protocol(fake_fields)

        # we can pass None for protocol_container and protocol_bits
        # because they are not being used here (see umpa.Packet)
        assert p._raw(0, 0, None, None) == (0x010101, 24)
        p.get_field('a').bits = 4
        assert p._raw(0, 0, None, None) == (0x010101, 20)
        p.get_field('a').bits = 8
        p.a = 16
        assert p._raw(0, 0, None, None) == (0x100101, 24)

        Protocol._pre_raw = old_pre
        Protocol._post_raw = old_post

    def test_get_raw(self):
        fake_fields = [IntField('foobar', 1, 8), IntField('foobar', 1, 8), 
                                                IntField('foobar', 1, 8)]
        fake_ordered = ('a', 'b', 'c')
        Protocol._ordered_fields = fake_ordered

        old_pre = Protocol._pre_raw
        old_post = Protocol._post_raw
        def fake_fun(*args):
            return args[1], args[2]
        Protocol._pre_raw = fake_fun
        Protocol._post_raw = fake_fun

        p = Protocol(fake_fields)

        # we can pass None for protocol_container and protocol_bits
        # because they are not being used here (see umpa.Packet)
        assert p.get_raw(None, None) == (0x010101, 24)
        p.get_field('a').bits = 8
        p.a = 16
        assert p.get_raw(None, None) == (0x100101, 24)

        p.get_field('a').bits = 4
        py.test.raises(UMPAException, p.get_raw, None, None)

        Protocol._pre_raw = old_pre
        Protocol._post_raw = old_post
