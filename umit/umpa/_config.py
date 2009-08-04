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

# __________________________
# libpcap wrapper

try:
    import pcap
    if hasattr(pcap, 'pcap'):
        libpcap = 'pypcap'
    elif hasattr(pcap, 'pcapObject'):
        libpcap = 'pylibpcap'
    else:
        libpcap = None
except ImportError:
    try:
        import pcapy
        libpcap = 'pcapy'
    except ImportError:
        libpcap = None

config = {
    'libpcap' : libpcap,
}

del libpcap
