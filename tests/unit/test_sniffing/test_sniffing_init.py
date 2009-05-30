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

import umpa
import umpa.sniffing
from umpa.protocols import IP, TCP
from tests.utils import SendPacket

class TestSniffing(object):
    def test_import_backend(self):
        assert hasattr(umpa.sniffing, 'lpcap')
        assert umpa.sniffing.lpcap._backend == umpa.config['libpcap']

    def test_get_available_devices(self):
        if umpa.config['libpcap'] == 'pypcap':
            from umpa.sniffing.libpcap import pypcap
            assert umpa.sniffing.get_available_devices()==pypcap.findalldevs()

    def test_sniff(self):
        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                    TCP(source_port=99)))
        th.start()
        result = umpa.sniffing.sniff(1, device='any')
        print result
