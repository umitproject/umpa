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

modulepath = "umpa.sniffing.libpcap.%s" % umpa.config['libpcap']
lpcap = __import__(modulepath, fromlist=[None])
lpcap._backend = umpa.config['libpcap']
del modulepath

def get_available_devices():
    """
    Return list of network devices.

    These devices are suitable for packets capturing.

    @note: There may be network devices that cannot be used for capturing
    because e.g. that process might not have sufficient privileges.
    
    @return: list of network devices
    """

    return lpcap.findalldevs()

def sniff(count, filter=None, device=None, callback=None, timeout=0,
                                        snaplen=1024, promisc=True):
    session = lpcap.open_live(device, snaplen, promisc, timeout)
    if filter:
        session.setfilter(filter)
    captured = []
    for i in xrange(count):
        captured.append(session.next())
    return captured

def sniff_any():
    pass

def sniff_next():
    pass

def from_file():
    pass

def to_file():
    pass
