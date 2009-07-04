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

import py.test

from umpa.protocols.Payload import _HData, Payload
from umpa.utils.exceptions import UMPAException
from tests.a_unit.test_protocols.test__fields import TestField

class TestHData(TestField):
    cls_field = _HData

    def test_init(self):
        f = self.cls_field('foobar')
        assert f.auto is False

        f = self.cls_field('foobar', 'xxx')
        assert f.get() == 'xxx'

    def test_get(self):
        f = self.cls_field('foobar', 10)
        assert f.get() == '10'
        
        f = self.cls_field('foobar')
        assert f.get() is None

    def test_set(self):
        f = self.cls_field('foobar', 'test')
        assert f.get() == 'test'

        f.set('foobarfoobar')
        assert f.get() == 'foobarfoobar'
        assert f.bits == 96

        f.set(123)
        assert f.get() == '123'
        assert f.bits == 24

        f.set(True)
        assert f.get() == 'True'
        assert f.bits == 32

        f.set(None)
        assert f.get() == 'None'
        assert f.bits == 32

    def test_clear(self):
        f = self.cls_field('foobar', 'test')
        f.set('foobarfoobar')
        assert f.get() == 'foobarfoobar'
        assert f.bits == 96
        f.clear()
        assert f.get() is None
        assert f.bits == 0

    def test_raw_value(self):
        f = self.cls_field('foobar', 'test')
        assert f.get() == 'test'
        assert f._raw_value() == 0x74657374

    def test_fillout(self):
        f = self.cls_field('foobar', 'test')
        assert f.fillout() == 0x74657374

        f = self.cls_field('foobar')
        py.test.raises(UMPAException, f.fillout)

class TestPayload(object):
    def test_init(self):
        p = Payload('test1')
        assert p.data == 'test1'

        p = Payload(data='test2')
        assert p.data == 'test2'

        p = Payload('test1', data='test2')
        assert p.data == 'test2'
