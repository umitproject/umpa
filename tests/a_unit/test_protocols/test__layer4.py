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

from umit.umpa.protocols import IP, TCP
from umit.umpa.protocols._layer4 import *
from umit.umpa.protocols._fields import *
from umit.umpa.utils.exceptions import UMPAException
from tests.a_unit.test_protocols.test__fields import TestIntField

class TestLayer4ChecksumField(TestIntField):
    cls_field = Layer4ChecksumField

    def test_init(self):
        f = self.cls_field('foobar')
        assert f.auto

    def test_fillout(self):
        f = self.cls_field('foobar')
        assert f.fillout() == 0
        f = self.cls_field('foobar', 10)
        assert f.fillout() == 10

class TestPseudoHeader(object):
    def test_pre_raw(self):
        p = PseudoHeader(0, 40)
        p._pre_raw(0, 0, [], 0)
        assert p.src == "127.0.0.1"
        assert p.dst == "127.0.0.1"

        p._pre_raw(0, 0, [IP(src="1.2.3.4")], 0)
        assert p.src == "1.2.3.4"
        assert p.dst == "127.0.0.1"

        p._pre_raw(0, 0, [IP(src="1.2.3.4",
                    dst="4.3.2.1"), TCP(srcport=123)], 0)
        assert p.src == "1.2.3.4"
        assert p.dst == "4.3.2.1"

        p._pre_raw(0, 0, [TCP(srcport=123)], 0)
        assert p.src == "127.0.0.1"
        assert p.dst == "127.0.0.1"
