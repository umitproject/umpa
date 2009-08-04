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

import os
import py.test

from umit.umpa import Socket, Packet
from umit.umpa.protocols import IP, TCP
from umit.umpa.utils.exceptions import UMPAException, UMPANotPermittedException


class TestUMPASockets(object):
    def test_init(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.raises(UMPANotPermittedException, "Socket()")

    def test_sent_size(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-priviliges are needed')

        p1 = Packet(IP(), TCP())
        p2 = Packet(IP(), TCP())

        s = Socket()
        size = s.send(p1, p2)

        assert size == [40, 40]
