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
from umpa.protocols import _consts

class TestConsts(object):
    if umpa.coding['libpcap'] == 'pypcap':
        from umpa.sniffing.libpcap import pypcap
        assert _consts.DLT_ARCNET == pypcap.pcap.DLT_ARCNET
        assert _consts.DLT_EN10MB == pypcap.pcap.DLT_EN10MB
        assert _consts.DLT_FDDI == pypcap.pcap.DLT_FDDI
        assert _consts.DLT_IEEE802 == pypcap.pcap.DLT_IEEE802
        assert _consts.DLT_LINUX_SLL == pypcap.pcap.DLT_LINUX_SLL
        assert _consts.DLT_LOOP == pypcap.pcap.DLT_LOOP
        assert _consts.DLT_NULL == pypcap.pcap.DLT_NULL
        assert _consts.DLT_PPP == pypcap.pcap.DLT_PPP
        assert _consts.DLT_RAW == pypcap.pcap.DLT_RAW
        assert _consts.DLT_SLIP == pypcap.pcap.DLT_SLIP
