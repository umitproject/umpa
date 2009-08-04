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

from umit.umpa.protocols import IP

class TestIP(object):
    def test_get_raw(self):
        py.test.skip('auto fields for IP have to implemented '
                    'first (like Identification)')
        # TODO more tests would be nice
        # this test pre/post raw methods as well
        ip = IP(src='127.0.0.1', dst='127.0.0.1')

        assert ip._raw(0, 0, [ip], 0) == \
                (0x450000149aa900004000e23e7f0000017f000001, 160)
