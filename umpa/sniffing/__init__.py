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

wrapper = umpa.config['libpcap']
modulepath = "umpa.sniffing.libpcap.%s" % wrapper
lpcap = __import__(modulepath, fromlist=[None])
lpcap._backend = wrapper

def get_available_devices():
    """
    REturn list of network devices.

    These devices are suitable for packets capturing.

    @note: There may be network devices that cannot be used for capturing
    because e.g. that process might not have sufficent priviliges.
    
    @return: list of network devices
    """

    return libpcap.findalldevs()
