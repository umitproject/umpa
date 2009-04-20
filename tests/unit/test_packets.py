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
from umpa.utils.exceptions import UMPAException

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
